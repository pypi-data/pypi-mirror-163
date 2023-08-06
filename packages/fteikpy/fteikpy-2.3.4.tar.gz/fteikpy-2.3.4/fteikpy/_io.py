import numpy as np

from ._grid import TraveltimeGrid2D, TraveltimeGrid3D
from ._solver import Eikonal2D, Eikonal3D


def grid_to_meshio(*args):
    """
    Return a :class:`meshio.Mesh` object from grids.

    Parameters
    ----------
    args : grid_like
        Grid objects to convert to mesh. Should be one of:

         - :class:`fteikpy.Eikonal2D`
         - :class:`fteikpy.Eikonal3D`
         - :class:`fteikpy.TraveltimeGrid2D`
         - :class:`fteikpy.TraveltimeGrid3D`

    Returns
    -------
    :class:`meshio.Mesh`
        Output mesh.

    """
    import meshio

    for i, arg in enumerate(args):
        if not isinstance(
            arg, (Eikonal2D, Eikonal3D, TraveltimeGrid2D, TraveltimeGrid3D)
        ):
            raise ValueError(f"argument {i + 1} is not a supported grid")

        if i == 0:
            ndim = arg._ndim
            shape = arg.shape
            gridsize = arg.gridsize
            origin = arg.origin

    # Generate mesh
    if ndim == 2:
        nz, nx = shape
        dz, dx = gridsize
        z0, x0 = origin

        if isinstance(args[0], TraveltimeGrid2D):
            nz -= 1
            nx -= 1

        points, cells = _generate_mesh_2d(nx, nz, dx, dz, x0, z0)

        # Append third dimension and swap axes
        points = np.column_stack((points, np.zeros(len(points))))
        points = points[:, [0, 2, 1]]

    else:
        nz, nx, ny = shape
        dz, dx, dy = gridsize
        z0, x0, y0 = origin

        if isinstance(args[0], TraveltimeGrid3D):
            nz -= 1
            nx -= 1
            ny -= 1

        points, cells = _generate_mesh_3d(nx, ny, nz, dx, dy, dz, x0, y0, z0)

    # Invert z-axis (depth -> elevation)
    points[:, 2] *= -1.0

    # Generate data arrays
    point_data = {}
    cell_data = {}
    vel_count = 0
    tt_count = 0

    for arg in args:
        # Velocity model
        if isinstance(arg, (Eikonal2D, Eikonal3D)):
            vel_count += 1

            name = f"Velocity {vel_count}" if vel_count > 1 else "Velocity"
            cell_data[name] = [_ravel_grid(arg.grid, ndim)]

        # Traveltime grid
        elif isinstance(arg, (TraveltimeGrid2D, TraveltimeGrid3D)):
            tt_count += 1

            name = f"Traveltime {tt_count}" if tt_count > 1 else "Traveltime"
            point_data[name] = _ravel_grid(arg.grid, ndim)

            # Gradient grid
            if arg._gradient is not None:
                name = f"Gradient {tt_count}" if tt_count > 1 else "Gradient"
                gradient = np.column_stack(
                    [_ravel_grid(grad.grid, ndim) for grad in arg.gradient]
                )

                if ndim == 2:
                    gradient = np.column_stack((gradient, np.zeros(len(points))))
                gradient = gradient[:, [1, 2, 0]]
                gradient[:, 2] *= -1.0
                point_data[name] = gradient

    return meshio.Mesh(points, cells, point_data, cell_data)


def ray_to_meshio(*args):
    """
    Return a :class:`meshio.Mesh` object from raypaths.

    Parameters
    ----------
    args : array_like
        Raypaths to convert to mesh.

    Returns
    -------
    :class:`meshio.Mesh`
        Output mesh.

    """
    import meshio

    for i, arg in enumerate(args):
        if np.ndim(arg) != 2:
            raise ValueError(f"argument {i + 1} does not seem to be a ray")

        if i == 0:
            ndim = np.shape(arg)[1]

    # Generate points and cells
    points = []
    cells = []

    for ray in args:
        cell = np.arange(len(ray)) + len(points)
        cells.append(("line", np.column_stack((cell[:-1], cell[1:]))))
        points = np.array(ray) if len(points) == 0 else np.row_stack((points, ray))

    # Swap axes (Z, X, Y -> X, Y, Z)
    points = (
        np.column_stack((points, np.zeros(len(points))))
        if ndim == 2
        else np.array(points)
    )
    points = points[:, [1, 2, 0]]

    # Invert z-axis (depth -> elevation)
    points[:, 2] *= -1.0

    return meshio.Mesh(points, cells)


def _generate_mesh_2d(nx, ny, dx, dy, x0, y0, order="F"):
    """Generate 2D structured grid."""
    # Internal functions
    def meshgrid(x, y, indexing="ij", order=order):
        """Generate mesh grid."""
        X, Y = np.meshgrid(x, y, indexing=indexing)
        return X.ravel(order), Y.ravel(order)

    def mesh_vertices(i, j):
        """Generate vertices for each quad."""
        return [
            [i, j],
            [i + 1, j],
            [i + 1, j + 1],
            [i, j + 1],
        ]

    # Grid
    dx = np.arange(nx + 1) * dx + x0
    dy = np.arange(ny + 1) * dy + y0
    xy_shape = [nx + 1, ny + 1]
    ij_shape = [nx, ny]
    X, Y = meshgrid(dx, dy)
    I, J = meshgrid(*[np.arange(n) for n in ij_shape])

    # Points and cells
    points = [[x, y] for x, y in zip(X, Y)]
    cells = [
        [
            np.ravel_multi_index(vertex, xy_shape, order=order)
            for vertex in mesh_vertices(i, j)
        ]
        for i, j in zip(I, J)
    ]

    return np.array(points, dtype=float), [("quad", np.array(cells))]


def _generate_mesh_3d(nx, ny, nz, dx, dy, dz, x0, y0, z0):
    """Generate 3D structured grid."""
    # Internal functions
    def meshgrid(x, y, z, indexing="ij", order="C"):
        """Generate mesh grid."""
        X, Y, Z = np.meshgrid(x, y, z, indexing=indexing)
        return X.ravel(order), Y.ravel(order), Z.ravel(order)

    def mesh_vertices(i, j, k):
        """Generate vertices for each hexahedron."""
        return [
            [i, j, k],
            [i + 1, j, k],
            [i + 1, j + 1, k],
            [i, j + 1, k],
            [i, j, k + 1],
            [i + 1, j, k + 1],
            [i + 1, j + 1, k + 1],
            [i, j + 1, k + 1],
        ]

    # Grid
    dx = np.arange(nx + 1) * dx + x0
    dy = np.arange(ny + 1) * dy + y0
    dz = np.arange(nz + 1) * dz + z0
    xyz_shape = [nx + 1, ny + 1, nz + 1]
    ijk_shape = [nx, ny, nz]
    X, Y, Z = meshgrid(dx, dy, dz)
    I, J, K = meshgrid(*[np.arange(n) for n in ijk_shape])

    # Points and cells
    points = [[x, y, z] for x, y, z in zip(X, Y, Z)]
    cells = [
        [
            np.ravel_multi_index(vertex, xyz_shape, order="C")
            for vertex in mesh_vertices(i, j, k)
        ]
        for i, j, k in zip(I, J, K)
    ]

    return (
        np.array(points, dtype=float),
        [("hexahedron", np.array(cells))],
    )


def _ravel_grid(grid, ndim):
    """Ravel grid."""
    return grid.ravel() if ndim == 2 else np.transpose(grid, axes=[1, 2, 0]).ravel()
