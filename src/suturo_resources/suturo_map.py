import numpy as np
from semantic_digital_twin.adapters.ros.visualization.viz_marker import (
    VizMarkerPublisher,
)
from semantic_digital_twin.semantic_annotations.semantic_annotations import (
    Table,
    Sofa,
    TrashCan,
    Fridge, Counter_Top, Wall, Cabinet, Cupboard, ShelfLayer, Hinge, Door, Handle, DiningTable, Leg, Drawer,
)
from semantic_digital_twin.world_description.degree_of_freedom import DegreeOfFreedomLimits
from semantic_digital_twin.spatial_types.derivatives import DerivativeMap
from semantic_digital_twin.world_description.connections import FixedConnection, RevoluteConnection, PrismaticConnection
from semantic_digital_twin.spatial_types.spatial_types import Vector3
from semantic_digital_twin.world import World
import threading
import rclpy
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.semantic_annotations.semantic_annotations import Room, Floor
from semantic_digital_twin.spatial_types.spatial_types import (
    HomogeneousTransformationMatrix,
    Point3,
)
from semantic_digital_twin.world_description.connections import FixedConnection
from semantic_digital_twin.world_description.geometry import Box, Scale, Color
from semantic_digital_twin.world_description.geometry import Cylinder
from semantic_digital_twin.world_description.shape_collection import ShapeCollection
from semantic_digital_twin.world_description.world_entity import Body

def load_environment():
    """
    Initializes the world with a hierarchical scene graph containing walls, furniture, and room layouts.
    Returns the constructed World object representing the environment.
    """
    world = World()
    root = Body(name=PrefixedName("root"))
    with world.modify_world():
        world.add_body(root)

    build_environment_walls(world)
    build_environment_furniture(world)
    build_environment_rooms(world)

    return world


def build_environment_walls(world: World):
    """
    Creates and connects all walls of the environment to the scene graph.
    The walls are represented as Body objects connected via FixedConnections.
    Returns the updated World object with walls integrated.
    """
    root = world.root
    root_transformation = HomogeneousTransformationMatrix.from_xyz_rpy(
        x=0.33, y=0.28, yaw=0.10707963267
    )

    with world.modify_world():
        south_wall1 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall1"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                y=-2.01
            ),
            scale=Scale(x=0.05, y=1.00, z=3.00),
        )

        south_wall2 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall2"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.145, y=-1.45, yaw=np.pi/2
            ),
            scale=Scale(x=0.05, y=0.29, z=3.00),
        )

        south_wall3 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall3"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.29, y=-0.9925
            ),
            scale=Scale(x=0.05, y=1.085, z=1.00),
        )

        south_wall4 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall4"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.145, y=-0.45, yaw=np.pi/2
            ),
            scale=Scale(x=0.05, y=0.29, z=1.00),
        )

        south_wall5 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall5"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.145, y=0.45, yaw=np.pi/2
            ),
            scale=Scale(0.05, 0.29, 1.00),
        )

        south_wall6 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall6"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.29025, y=1.80
            ),
            scale=Scale(0.05, 2.75, 1.00),
        )

        south_wall7 = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("south_wall7"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=-0.29025, y=5.16
            ),
            scale=Scale(0.05, 2.27, 1.00),
        )

        east_wall = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("east_wall"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=2.462, y=-2.535, yaw=np.pi/2
            ),
            scale=Scale(0.05, 4.924, 3.00),
        )

        middle_wall = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("middle_wall"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=2.20975, y=5.00
            ),
            scale=Scale(0.05, 2.67, 1.00),
        )

        west_wall = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("west_wall"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=1.9345, y=6.32, yaw=np.pi/2
            ),
            scale=Scale(0.05, 4.449, 3.00),
        )

        north_wall = Wall.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("north_wall"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=4.949, y=1.51
            ),
            scale=Scale(0.05, 8.04, 3.00),
        )

    north_west_wall = Cylinder(width=1.53, height=3.00)
    shape_geometry = ShapeCollection([north_west_wall])
    north_west_wall_body = Body(
        name=PrefixedName("north_west_wall_body"),
        collision=shape_geometry,
        visual=shape_geometry,
    )

    root_C_north_west_wall = FixedConnection(
        parent=root,
        child=north_west_wall_body,
        parent_T_connection_expression=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
            x=4.924, y=6.295, z=1.50
        ),
    )

    with world.modify_world():
        world.add_connection(root_C_north_west_wall)
        return world


def build_environment_furniture(world: World):
    """
    Adds furniture items and room layouts (kitchen, living room, bedroom, office) to the scene graph.
    Connects furniture bodies and room structures hierarchically under the main root.
    Returns the updated World object with furniture integrated.
    """
    # all_elements_connections = []
    root = world.root

    root_transformation = HomogeneousTransformationMatrix.from_xyz_rpy(
        x=0.33, y=0.28, yaw=0.10707963267
    )

    ovenArea = Box(scale=Scale(1.20, 0.658, 1.49))
    shape_geometry = ShapeCollection([ovenArea])
    ovenArea_body = Body(
        name=PrefixedName("ovenArea_body"),
        collision=shape_geometry,
        visual=shape_geometry,
    )

    root_C_ovenArea = FixedConnection(
        parent=root,
        child=ovenArea_body,
        parent_T_connection_expression=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
            x=3.481, y=-2.181, z=0.745
        ),
    )

    with world.modify_world():
        trash_can = TrashCan.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("trash_can"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                x=0.416, y=5.5, z=0.20
            ),
            scale=Scale(x=0.30, y=0.30, z=0.40),
        )

        refrigerator = Fridge.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("refrigerator"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(
                 x=0.537, y=-2.181, z=0.745, yaw=np.pi*3/2),
            scale=Scale(x=0.60, y=0.658, z=1.49),
        )

        counterTop = Counter_Top.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("counterTop"),
            world_root_T_self= root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=1.859, y=-2.181, z=0.2725),
            scale=Scale(x=2.044, y=0.658, z=0.545),
        )
        for color in counterTop.bodies[0].visual.shapes:
            color.color = Color.BEIGE()


        table = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("table"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=3.545, y=0.426, z=0.4225),
            scale=Scale(x=2.45, y=0.796, z=0.845),
        )

        sofa = Sofa.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("sofa"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=3.60, y=1.20, z=0.34, yaw=4.7124),
            scale=Scale(x=0.94, y=1.68, z=0.68),
        )
        for color in sofa.bodies[0].visual.shapes:
            color.color = Color.BEIGE()

        lowerTable = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("lowerTable"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=4.22, y=2.22, z=0.22),
            scale=Scale(x=0.37, y=0.91, z=0.44),
        )

        cupboard_scale = Scale(0.43, 0.80, 2.02)

        cupboard = Cupboard.create_with_new_body_in_world(
            name=PrefixedName("cupboard_annotation"),
            world=world,
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=4.55, y=4.72, z=1.01),
            scale=cupboard_scale,
            wall_thickness=0.02,
        )
        # Connect the cupboard tp 'root' , to ensure that the coordinates are relative to the room
        cupboard_connection = cupboard.root.parent_connection
        world.remove_connection(cupboard_connection)
        cupboard_connection.parent = root
        world.add_connection(cupboard_connection)

        # create shelflayers manually and attach them directly to the cupboard
        shelf_scale = Scale(0.40, 0.76, 0.02)

        # Shelf 1
        shelf_1_geom = ShapeCollection([Box(scale=shelf_scale, color=Color.WHITE())])
        shelf_1_body = Body(
            name=PrefixedName("cupboard_shelf_1_body"),
            collision=shelf_1_geom,
            visual=shelf_1_geom,
        )
        shelf_1 = ShelfLayer(root=shelf_1_body, name=PrefixedName("cupboard_shelf_1"))

        cupboard_C_shelf_1 = FixedConnection(
            parent=cupboard.root,
            child=shelf_1_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=0, y=0, z=-0.5
            ),
        )
        world.add_connection(cupboard_C_shelf_1)
        world.add_semantic_annotation(shelf_1)
        cupboard.add_shelf_layer(shelf_1)

        # Shelf 2
        shelf_2_geom = ShapeCollection([Box(scale=shelf_scale, color=Color.WHITE())])
        shelf_2_body = Body(
            name=PrefixedName("cupboard_shelf_2_body"),
            collision=shelf_2_geom,
            visual=shelf_2_geom,
        )
        shelf_2 = ShelfLayer(root=shelf_2_body, name=PrefixedName("cupboard_shelf_2"))

        cupboard_C_shelf_2 = FixedConnection(
            parent=cupboard.root,
            child=shelf_2_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=0, y=0, z=0.5
            ),
        )
        world.add_connection(cupboard_C_shelf_2)
        world.add_semantic_annotation(shelf_2)
        cupboard.add_shelf_layer(shelf_2)

        # Creating doors manually and attaching them directly to the cupboard
        # Door height 105.5 cm (1.055 m)
        door_height = 1.055
        # Position Z: Bottom of cupboard is at -cupboard_scale.z / 2.
        # Door center should be at Bottom + door_height / 2
        door_z_rel = -(cupboard_scale.z / 2) + (door_height / 2)

        door_x_rel = -(cupboard_scale.x / 2) - 0.01
        door_scale = Scale(0.02, 0.40, door_height)

        # Define limits for doors
        # Left door opens outwards (0 to +90 degrees)
        left_lower = DerivativeMap[float](position=0.0)
        left_upper = DerivativeMap[float](position=np.pi / 2)
        left_door_limits = DegreeOfFreedomLimits(lower=left_lower, upper=left_upper)

        # Right door opens outwards (-90 to 0 degrees)
        right_lower = DerivativeMap[float](position=-np.pi / 2)
        right_upper = DerivativeMap[float](position=0.0)
        right_door_limits = DegreeOfFreedomLimits(lower=right_lower, upper=right_upper)

        # Left Door (Open via Hinge)
        # Create Hinge for the left door
        hinge_left_body = Body(name=PrefixedName("cupboard_hinge_left_body"))
        hinge_left = Hinge(
            root=hinge_left_body,
            name=PrefixedName("cupboard_hinge_left"),
        )

        cupboard_C_hinge_left = RevoluteConnection.create_with_dofs(
            world=world,
            parent=cupboard.root,
            child=hinge_left_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=door_x_rel, y=-0.40, z=door_z_rel
            ),
            axis=Vector3.Z(),
            dof_limits=left_door_limits,
        )
        world.add_connection(cupboard_C_hinge_left)
        world.add_semantic_annotation(hinge_left)

        # Create left door
        door_left_geom = ShapeCollection([Box(scale=door_scale, color=Color.WHITE())])
        door_left_body = Body(
            name=PrefixedName("cupboard_door_left_body"),
            collision=door_left_geom,
            visual=door_left_geom,
        )
        door_left = Door(root=door_left_body, name=PrefixedName("cupboard_door_left"))

        # Connect Door to Hinge (Fixed)
        # Door center is at y=+0.20 relative to hinge (hinge at -0.40, door center at -0.20)
        hinge_left_C_door_left = FixedConnection(
            parent=hinge_left_body,
            child=door_left_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=0, y=0.20, z=0
            ),
        )
        world.add_connection(hinge_left_C_door_left)
        world.add_semantic_annotation(door_left)
        door_left.add_hinge(hinge_left)

        # Handle for Left Door
        handle_scale = Scale(0.04, 0.04, 0.04)
        handle_left_geom = ShapeCollection([Box(scale=handle_scale, color=Color.GRAY())])
        handle_left_body = Body(name=PrefixedName("cupboard_handle_left_body"), collision=handle_left_geom, visual=handle_left_geom)
        handle_left = Handle(root=handle_left_body, name=PrefixedName("cupboard_handle_left"))
        
        # Position: near the opening edge (+y for left door) and centered vertically
        door_left_C_handle_left = FixedConnection(
            parent=door_left_body,
            child=handle_left_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-0.03, y=0.15, z=0)
        )
        world.add_connection(door_left_C_handle_left)
        world.add_semantic_annotation(handle_left)
        cupboard.add_door(door_left)

        # Right Door (Closed via Hinge)
        hinge_right_body = Body(name=PrefixedName("cupboard_hinge_right_body"))
        hinge_right = Hinge(
            root=hinge_right_body,
            name=PrefixedName("cupboard_hinge_right"),
        )

        cupboard_C_hinge_right = RevoluteConnection.create_with_dofs(
            world=world,
            parent=cupboard.root,
            child=hinge_right_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=door_x_rel, y=0.40, z=door_z_rel
            ),
            axis=Vector3.Z(),
            dof_limits=right_door_limits,
        )
        world.add_connection(cupboard_C_hinge_right)
        world.add_semantic_annotation(hinge_right)

        door_right_geom = ShapeCollection([Box(scale=door_scale, color=Color.WHITE())])
        door_right_body = Body(
            name=PrefixedName("cupboard_door_right_body"),
            collision=door_right_geom,
            visual=door_right_geom,
        )
        door_right = Door(root=door_right_body, name=PrefixedName("cupboard_door_right"))

        hinge_right_C_door_right = FixedConnection(
            parent=hinge_right_body,
            child=door_right_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(
                x=0, y=-0.20, z=0
            ),
        )
        world.add_connection(hinge_right_C_door_right)
        world.add_semantic_annotation(door_right)
        door_right.add_hinge(hinge_right)

        # Handle for Right Door
        handle_right_geom = ShapeCollection([Box(scale=handle_scale, color=Color.GRAY())])
        handle_right_body = Body(name=PrefixedName("cupboard_handle_right_body"), collision=handle_right_geom, visual=handle_right_geom)
        handle_right = Handle(root=handle_right_body, name=PrefixedName("cupboard_handle_right"))
        
        # Position: near the opening edge (-y for right door) and centered vertically
        door_right_C_handle_right = FixedConnection(
            parent=door_right_body,
            child=handle_right_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-0.03, y=-0.15, z=0)
        )
        world.add_connection(door_right_C_handle_right)
        world.add_semantic_annotation(handle_right)
        cupboard.add_door(door_right)

        desk = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("desk"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=0.05, y=1.28, z=0.375),
            scale=Scale(x=0.60, y=1.20, z=0.75),
        )

        # --- MODULAR COOKING TABLE --- 
        ct_l, ct_d, ct_h, ct_thick = 1.75, 0.64, 0.71, 0.04
        # 1. Top Layer (The Worktop)
        cooking_table = Table.create_with_new_body_in_world(world=world, name=PrefixedName("cooking_table"), world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=1.325, y=5.99, z=ct_h), scale=Scale(ct_l, ct_d, ct_thick))
        for s in cooking_table.bodies[0].visual.shapes: s.color = Color.BEIGE()
        
        # Ceran Field
        cooktop_body = Body(name=PrefixedName("cooktop_body"))
        cooktop_geom = ShapeCollection([Box(scale=Scale(0.5,0.5,0.01), color=Color.BLACK())], reference_frame=cooktop_body)
        cooktop_geom.transform_all_shapes_to_own_frame()
        cooktop_body.collision, cooktop_body.visual = cooktop_geom, cooktop_geom
        world.add_connection(FixedConnection(parent=cooking_table.root, child=cooktop_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=ct_thick/2 + 0.005)))

        # 2. Bottom Layer (The Support)
        ct_bottom_body = Body(name=PrefixedName("cooking_table_bottom_body"))
        ct_bottom_geom = ShapeCollection([Box(scale=Scale(ct_l, ct_d, ct_thick), color=Color.BEIGE())], reference_frame=ct_bottom_body)
        ct_bottom_geom.transform_all_shapes_to_own_frame()
        ct_bottom_body.collision, ct_bottom_body.visual = ct_bottom_geom, ct_bottom_geom
        world.add_connection(FixedConnection(parent=cooking_table.root, child=ct_bottom_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-ct_h + ct_thick)))

        # 3. Side Modules (Cupboards with Drawers)
        mod_w = (ct_l - 0.60) / 2
        dr_limits = DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=0.40))
        for side in [-1, 1]:
            s_n = "left" if side == -1 else "right"
            # Module Cupboard
            mod_cupboard = Cupboard.create_with_new_body_in_world(name=PrefixedName(f"cooking_mod_{s_n}"), world=world, scale=Scale(mod_w, ct_d, ct_h - 2*ct_thick))
            for s in mod_cupboard.bodies[0].visual.shapes: s.color = Color.WHITE()
            world.remove_connection(mod_cupboard.root.parent_connection)
            world.add_connection(FixedConnection(parent=cooking_table.root, child=mod_cupboard.root, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=side*(0.3+mod_w/2), z=-ct_h/2 + ct_thick, yaw=1.5708)))
            
            # Drawer in Module
            dr_body = Body(name=PrefixedName(f"cooking_drawer_{s_n}_body"))
            dr_geom = ShapeCollection([Box(scale=Scale(mod_w-0.04, ct_d-0.05, 0.15), color=Color.BEIGE())], reference_frame=dr_body)
            dr_geom.transform_all_shapes_to_own_frame()
            dr_body.collision, dr_body.visual = dr_geom, dr_geom
            drawer = Drawer(root=dr_body, name=PrefixedName(f"cooking_drawer_{s_n}"))
            world.add_connection(PrismaticConnection.create_with_dofs(world=world, parent=mod_cupboard.root, child=dr_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=0.2), axis=Vector3.Y(), dof_limits=dr_limits))
            world.add_semantic_annotation(drawer)
            
            # Drawer Handle (Rectangular)
            ha_body = Body(name=PrefixedName(f"cooking_drawer_handle_{s_n}_body"))
            ha_geom = ShapeCollection([Box(scale=Scale(0.02, mod_w/3, 0.04), color=Color.GRAY())], reference_frame=ha_body)
            ha_geom.transform_all_shapes_to_own_frame()
            ha_body.collision, ha_body.visual = ha_geom, ha_geom
            handle = Handle(root=ha_body, name=PrefixedName(f"cooking_drawer_handle_{s_n}"))
            world.add_connection(FixedConnection(parent=dr_body, child=ha_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-mod_w/2)))
            world.add_semantic_annotation(handle)
            drawer.add_handle(handle)
            
            # Shelf below Drawer
            sh_body = Body(name=PrefixedName(f"cooking_shelf_{s_n}_body"))
            sh_geom = ShapeCollection([Box(scale=Scale(mod_w-0.04, ct_d-0.05, 0.02), color=Color.WHITE())], reference_frame=sh_body)
            sh_geom.transform_all_shapes_to_own_frame()
            sh_body.collision, sh_body.visual = sh_geom, sh_geom
            shelf = ShelfLayer(root=sh_body, name=PrefixedName(f"cooking_shelf_{s_n}"))
            world.add_connection(FixedConnection(parent=mod_cupboard.root, child=sh_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-0.1)))
            world.add_semantic_annotation(shelf)
            mod_cupboard.add_shelf_layer(shelf)

        # Dining Table Construction
        dt_length, dt_width, dt_height = 0.73, 1.18, 0.76
        dt_color = Color.BEIGE()
        dt_plate_thickness = 0.04
        
        dining_table = DiningTable.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("dining_table"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=2.59975, y=5.705, z=0.76),
            scale=Scale(dt_length, dt_width, dt_plate_thickness),
        )
        for shape in dining_table.root.visual.shapes: shape.color = dt_color

        leg_scale = Scale(0.06, 0.06, dt_height - dt_plate_thickness)
        x_offset = (dt_length / 2) - 0.03
        y_offset = (dt_width / 2) - 0.03
        z_pos = -(dt_plate_thickness / 2) - (leg_scale.z / 2)

        for i, (sign_x, sign_y) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
            l_body = Body(name=PrefixedName(f"dining_table_leg_{i}_body"))
            leg = Leg(root=l_body, name=PrefixedName(f"dining_table_leg_{i}"))
            l_geom = ShapeCollection([Box(scale=leg_scale, color=dt_color)], reference_frame=l_body)
            l_geom.transform_all_shapes_to_own_frame()
            l_body.collision = l_geom
            l_body.visual = l_geom
            # Create connection and add to world
            world.add_connection(FixedConnection(
                parent=dining_table.root,
                child=l_body,
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=sign_x * x_offset, y=sign_y * y_offset, z=z_pos)
            ))
            world.add_semantic_annotation(leg)
            dining_table.add_leg(leg)

        world.add_connection(root_C_ovenArea)
    return world


def build_environment_rooms(world: World):

    room_annotations = []

    root_transformation = HomogeneousTransformationMatrix.from_xyz_rpy(
        x=0.33, y=0.28, yaw=0.10707963267
    )

    with world.modify_world():
        kitchen_floor_polytope = [
            Point3(0, 0, 0),
            Point3(0, 3.334, 0),
            Point3(5.214, 3.334, 0),
            Point3(5.214, 0, 0),
        ]

        living_room_floor_polytope = [
            Point3(0, 0, 0),
            Point3(0, 2.971, 0),
            Point3(5.214, 2.971, 0),
            Point3(5.214, 0, 0),
        ]

        bed_room_floor_polytope = [
            Point3(0, 0, 0),
            Point3(0, 2.67, 0.0),
            Point3(2.50, 2.67, 0.0),
            Point3(2.50, 0, 0.0),
        ]

        office_floor_polytope = [
            Point3(0, 0, 0),
            Point3(0, 2.67, 0),
            Point3(2.71, 2.67, 0),
            Point3(2.71, 0, 0),
        ]

        kitchen_floor = Floor.create_with_new_body_from_polytope_in_world(
            name=PrefixedName("kitchen_floor"),
            world=world,
            floor_polytope=kitchen_floor_polytope,
            world_root_T_self=root_transformation
            @ HomogeneousTransformationMatrix.from_xyz_rpy(x=2.317, y=-0.843),
        )
        kitchen = Room(floor=kitchen_floor, name=PrefixedName("kitchen"))
        room_annotations.append(kitchen)

        living_room_floor = Floor.create_with_new_body_from_polytope_in_world(
            name=PrefixedName("living_room_floor"),
            world=world,
            floor_polytope=living_room_floor_polytope,
            world_root_T_self=root_transformation
            @ HomogeneousTransformationMatrix.from_xyz_rpy(x=2.317, y=2.3095),
        )
        living_room = Room(floor=living_room_floor, name=PrefixedName("living_room"))
        room_annotations.append(living_room)

        bed_room_floor = Floor.create_with_new_body_from_polytope_in_world(
            name=PrefixedName("bed_room_floor"),
            world=world,
            floor_polytope=bed_room_floor_polytope,
            world_root_T_self=root_transformation
            @ HomogeneousTransformationMatrix.from_xyz_rpy(x=0.96, y=4.96),
        )
        bed_room = Room(floor=bed_room_floor, name=PrefixedName("bed_room"))
        room_annotations.append(bed_room)

        office_floor = Floor.create_with_new_body_from_polytope_in_world(
            name=PrefixedName("office_floor"),
            world=world,
            floor_polytope=office_floor_polytope,
            world_root_T_self=root_transformation
            @ HomogeneousTransformationMatrix.from_xyz_rpy(x=3.56, y=4.96),
        )
        office = Room(floor=office_floor, name=PrefixedName("office"))
        room_annotations.append(office)

        world.add_semantic_annotations(room_annotations)

    return world


class Publisher:
    def __init__(self, name):
        self.context = rclpy.init()
        self.node = rclpy.create_node(name)
        self.thread = threading.Thread(
            target=rclpy.spin, args=(self.node,), daemon=True
        )
        self.thread.start()

    def publish(self, world):
        viz = VizMarkerPublisher(_world=world, node=self.node)
        viz.notify()
        viz.with_tf_publisher()
