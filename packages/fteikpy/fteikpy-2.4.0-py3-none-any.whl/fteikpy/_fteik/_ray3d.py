import numpy as np
from numba import prange

from .._common import dist3d, jitted, norm3d
from .._interp import interp3d
from ._common import shrink


@jitted(
    "Tuple((f8[:, :], i4))(f8[:], f8[:], f8[:], f8[:, :, :], f8[:, :, :], f8[:, :, :], f8, f8, f8, f8, f8, f8, f8, i4, b1)"
)
def _ray3d(
    z,
    x,
    y,
    zgrad,
    xgrad,
    ygrad,
    zend,
    xend,
    yend,
    zsrc,
    xsrc,
    ysrc,
    stepsize,
    max_step,
    honor_grid,
):
    """Perform a posteriori 3D ray-tracing."""
    condz = z[0] <= zend <= z[-1]
    condx = x[0] <= xend <= x[-1]
    condy = y[0] <= yend <= y[-1]
    if not (condz and condx and condy):
        raise ValueError("end point out of bound")

    if honor_grid:
        nz, nx, ny = len(z), len(x), len(y)

        i = np.searchsorted(z, zend, side="right") - 1
        j = np.searchsorted(x, xend, side="right") - 1
        k = np.searchsorted(y, yend, side="right") - 1
        zmin = z[max(i - 1, 0)] if zend == z[i] else z[i]
        xmin = x[max(j - 1, 0)] if xend == x[j] else x[j]
        ymin = y[max(k - 1, 0)] if yend == y[k] else y[k]
        lower = np.array([zmin, xmin, ymin])
        upper = np.array(
            [z[min(i + 1, nz - 1)], x[min(j + 1, nx - 1)], y[min(k + 1, ny - 1)]]
        )

        isrc = np.searchsorted(z, zsrc, side="right") - 1
        jsrc = np.searchsorted(x, xsrc, side="right") - 1
        ksrc = np.searchsorted(y, ysrc, side="right") - 1

    count = 1
    pcur = np.array([zend, xend, yend], dtype=np.float64)
    delta = np.empty(3, dtype=np.float64)
    ray = np.empty((max_step, 3), dtype=np.float64)
    ray[0] = pcur.copy()
    while dist3d(zsrc, xsrc, ysrc, pcur[0], pcur[1], pcur[2]) >= stepsize:
        gz = interp3d(z, x, y, zgrad, pcur)
        gx = interp3d(z, x, y, xgrad, pcur)
        gy = interp3d(z, x, y, ygrad, pcur)
        gn = norm3d(gz, gx, gy)

        if gn > 0.0:
            gni = 1.0 / gn
        else:
            break

        delta[0] = stepsize * gz * gni
        delta[1] = stepsize * gx * gni
        delta[2] = stepsize * gy * gni

        if honor_grid:
            fac = shrink(pcur, delta, lower, upper)
            pcur -= fac * delta
            pcur[0] = min(max(pcur[0], z[0]), z[-1])
            pcur[1] = min(max(pcur[1], x[0]), x[-1])
            pcur[2] = min(max(pcur[2], y[0]), y[-1])

            if fac < 1.0:
                # Grid magnetism: handle precision issues due to fac
                for ix in range(3):
                    if np.abs(pcur[ix] - lower[ix]) < 1.0e-8:
                        pcur[ix] = lower[ix]

                    elif np.abs(pcur[ix] - upper[ix]) < 1.0e-8:
                        pcur[ix] = upper[ix]

                i = np.searchsorted(z, pcur[0], side="right") - 1
                j = np.searchsorted(x, pcur[1], side="right") - 1
                k = np.searchsorted(y, pcur[2], side="right") - 1
                lower[0] = z[max(i - 1, 0)] if pcur[0] == z[i] else z[i]
                lower[1] = x[max(j - 1, 0)] if pcur[1] == x[j] else x[j]
                lower[2] = y[max(k - 1, 0)] if pcur[2] == y[k] else y[k]
                upper[0] = z[i + 1]
                upper[1] = x[j + 1]
                upper[2] = y[k + 1]

                ray[count] = pcur.copy()
                count += 1

                if i == isrc and j == jsrc and k == ksrc:
                    break

        else:
            pcur -= delta
            pcur[0] = min(max(pcur[0], z[0]), z[-1])
            pcur[1] = min(max(pcur[1], x[0]), x[-1])
            pcur[2] = min(max(pcur[2], y[0]), y[-1])

            ray[count] = pcur.copy()
            count += 1

        if count >= max_step:
            raise RuntimeError("maximum number of steps reached")

    ray[count] = np.array([zsrc, xsrc, ysrc], dtype=np.float64)

    return ray, count


@jitted(parallel=True)
def _ray3d_vectorized(
    z,
    x,
    y,
    zgrad,
    xgrad,
    ygrad,
    zend,
    xend,
    yend,
    zsrc,
    xsrc,
    ysrc,
    stepsize,
    max_step,
    honor_grid=False,
):
    """Perform ray-tracing in parallel for different points."""
    n = len(zend)
    rays = np.empty((n, max_step, 3), dtype=np.float64)
    counts = np.empty(n, dtype=np.int32)
    for i in prange(n):
        rays[i], counts[i] = _ray3d(
            z,
            x,
            y,
            zgrad,
            xgrad,
            ygrad,
            zend[i],
            xend[i],
            yend[i],
            zsrc,
            xsrc,
            ysrc,
            stepsize,
            max_step,
            honor_grid,
        )

    return rays, counts


@jitted
def ray3d(z, x, y, zgrad, xgrad, ygrad, p, src, stepsize, max_step, honor_grid=False):
    """Perform ray-tracing."""
    if p.ndim == 1:
        ray, count = _ray3d(
            z,
            x,
            y,
            zgrad,
            xgrad,
            ygrad,
            p[0],
            p[1],
            p[2],
            src[0],
            src[1],
            src[2],
            stepsize,
            max_step,
            honor_grid,
        )
        return ray[count::-1]

    else:
        rays, counts = _ray3d_vectorized(
            z,
            x,
            y,
            zgrad,
            xgrad,
            ygrad,
            p[:, 0],
            p[:, 1],
            p[:, 2],
            src[0],
            src[1],
            src[2],
            stepsize,
            max_step,
            honor_grid,
        )
        return [ray[count::-1] for ray, count in zip(rays, counts)]
