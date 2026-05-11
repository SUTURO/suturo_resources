import numpy as np
from semantic_digital_twin.adapters.ros.visualization.viz_marker import (
    VizMarkerPublisher,
)
from semantic_digital_twin.semantic_annotations.semantic_annotations import (
    Table,
    Sofa,
    TrashCan,
    Fridge, Counter_Top, Wall, Cabinet, Cupboard, ShelfLayer, Hinge, Door, Handle, DiningTable, Leg, Drawer, Desk,
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



    with world.modify_world():
        # --- REFINED TRASH CAN ---
        tc_l, tc_w, tc_h = 0.30, 0.30, 0.40
        tc_root_T = root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=0.416, y=5.5, z=tc_h)
        
        trash_can = TrashCan.create_with_new_body_in_world(
            world=world, name=PrefixedName("trash_can"),
            world_root_T_self=tc_root_T, scale=Scale(tc_l, tc_w, 0.02))
        for s in trash_can.bodies[0].visual.shapes: s.color = Color.GRAY()

        # Bin Body
        bin_body = Body(name=PrefixedName("trash_bin_body"))
        bin_geom = ShapeCollection([Box(scale=Scale(tc_l, tc_w, tc_h), color=Color.GRAY())], reference_frame=bin_body)
        bin_geom.transform_all_shapes_to_own_frame()
        bin_body.collision, bin_body.visual = bin_geom, bin_geom
        world.add_connection(FixedConnection(parent=trash_can.root, child=bin_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-tc_h/2)))

        # Lid (Deckel)
        lid_h = 0.02
        lid_body = Body(name=PrefixedName("trash_lid_body"))
        lid_geom = ShapeCollection([Box(scale=Scale(tc_l, tc_w, lid_h), color=Color.BLACK())], reference_frame=lid_body)
        lid_geom.transform_all_shapes_to_own_frame()
        lid_body.collision, lid_body.visual = lid_geom, lid_geom
        
        lid_hinge = Body(name=PrefixedName("trash_lid_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=bin_body, child=lid_hinge,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-tc_l/2, z=tc_h/2),
            axis=Vector3.Y(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=-np.pi/2), upper=DerivativeMap[float](position=0.0))))
        world.add_connection(FixedConnection(parent=lid_hinge, child=lid_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=tc_l/2, z=lid_h/2)))

        # --- DETAILED REFRIGERATOR --- 
        fridge_l, fridge_w, fridge_h = 0.60, 0.658, 1.49
        fridge_color = Color.GRAY()
        
        refrigerator = Fridge.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("refrigerator"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=0.537, y=-2.181, z=fridge_h, yaw=np.pi/2),
            scale=Scale(fridge_l, fridge_w, 0.02) # Start with top plate as root
        )
        for s in refrigerator.bodies[0].visual.shapes: s.color = fridge_color

        # 1. Main Body (Static Frame)
        frame_body = Body(name=PrefixedName("fridge_frame_body"))
        frame_geom = ShapeCollection([Box(scale=Scale(fridge_l, fridge_w, fridge_h), color=fridge_color)], reference_frame=frame_body)
        frame_geom.transform_all_shapes_to_own_frame()
        frame_body.collision, frame_body.visual = frame_geom, frame_geom
        for s in frame_body.visual.shapes: s.color = Color.GRAY()
        world.add_connection(FixedConnection(parent=refrigerator.root, child=frame_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-fridge_h/2)))

        # 2. Upper Door (2/3 height)
        door_h = (fridge_h - 0.08) * 0.75
        door_body = Body(name=PrefixedName("fridge_door_body"))
        door_geom = ShapeCollection([Box(scale=Scale(0.02, fridge_w, door_h), color=Color.WHITE())], reference_frame=door_body)
        door_geom.transform_all_shapes_to_own_frame()
        door_body.collision, door_body.visual = door_geom, door_geom
        for s in door_body.visual.shapes: s.color = Color.WHITE()
        fridge_door = Door(root=door_body, name=PrefixedName("fridge_door"))
        
        # Hinge for Door
        hinge_body = Body(name=PrefixedName("fridge_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=frame_body, child=hinge_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=fridge_l/2, y=fridge_w/2, z=fridge_h/2 - door_h/2), 
            axis=Vector3.Z(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=np.pi/2))))
        world.add_connection(FixedConnection(parent=hinge_body, child=door_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=-fridge_w/2)))
        world.add_semantic_annotation(fridge_door)

        # 3. Lower Drawer (Optimized with White Front and Gray Case)
        drawer_h = (fridge_h - 0.08) * 0.25
        dr_body = Body(name=PrefixedName("fridge_drawer_body"))
        
        # Drawer Case (Gray)
        dr_case_l = fridge_l - 0.04
        dr_case_geom = Box(scale=Scale(dr_case_l, fridge_w-0.04, drawer_h-0.04), color=Color.GRAY())
        
        # Drawer Front (White)
        dr_front_thick = 0.02
        dr_front_geom = Box(scale=Scale(dr_front_thick, fridge_w, drawer_h), color=Color.WHITE())
        dr_front_geom.origin = HomogeneousTransformationMatrix.from_xyz_rpy(x=fridge_l/2 - dr_front_thick/2)
        
        dr_geom = ShapeCollection([dr_case_geom, dr_front_geom], reference_frame=dr_body)
        dr_geom.transform_all_shapes_to_own_frame()
        dr_body.collision, dr_body.visual = dr_geom, dr_geom
        fridge_drawer = Drawer(root=dr_body, name=PrefixedName("fridge_drawer"))
        
        world.add_connection(PrismaticConnection.create_with_dofs(world=world, parent=frame_body, child=dr_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-fridge_h/2 + 0.08 + drawer_h/2), 
            axis=Vector3.X(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=0.5))))
        world.add_semantic_annotation(fridge_drawer)

        # 4. Handles
        handle_scale = Scale(0.04, 0.02, door_h - 0.08)
        # Door Handle
        ha_door_body = Body(name=PrefixedName("fridge_door_handle_body"))
        ha_door_geom = ShapeCollection([Box(scale=handle_scale, color=Color.GRAY())], reference_frame=ha_door_body)
        ha_door_geom.transform_all_shapes_to_own_frame()
        ha_door_body.collision, ha_door_body.visual = ha_door_geom, ha_door_geom
        world.add_connection(FixedConnection(parent=door_body, child=ha_door_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=0.02, y=-fridge_w/2 + 0.03)))
        world.add_semantic_annotation(Handle(root=ha_door_body, name=PrefixedName("fridge_door_handle")))
        
        # Drawer Handle
        ha_dr_body = Body(name=PrefixedName("fridge_drawer_handle_body"))
        ha_dr_geom = ShapeCollection([Box(scale=Scale(0.04, 0.5, 0.02), color=Color.GRAY())], reference_frame=ha_dr_body)
        ha_dr_geom.transform_all_shapes_to_own_frame()
        ha_dr_body.collision, ha_dr_body.visual = ha_dr_geom, ha_dr_geom
        world.add_connection(FixedConnection(parent=dr_body, child=ha_dr_body, parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=fridge_l/2, z=drawer_h/2 - 0.03)))
        world.add_semantic_annotation(Handle(root=ha_dr_body, name=PrefixedName("fridge_drawer_handle")))

        # --- DETAILED KITCHEN COUNTER (3 Modules) ---
        ct_l, ct_d, ct_h = 2.044, 0.658, 0.6
        ct_color = Color.BEIGE()
        ct_root_T = root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=1.887, y=-2.181, z=ct_h)
        
        # Main Counter Annotation (using the top plate as root)
        counterTop = Counter_Top.create_with_new_body_in_world(
            world=world, name=PrefixedName("counterTop"),
            world_root_T_self=ct_root_T, scale=Scale(ct_l, ct_d, 0.04))
        for s in counterTop.bodies[0].visual.shapes: s.color = ct_color

        # 0. Sink (Waschbecken) - Visualized on the worktop
        sink_body = Body(name=PrefixedName("sink_body"))
        sink_geom = ShapeCollection([Box(scale=Scale(0.6, 0.4, 0.005), color=Color.BLACK())], reference_frame=sink_body)
        sink_geom.transform_all_shapes_to_own_frame()
        sink_body.collision, sink_body.visual = sink_geom, sink_geom
        world.add_connection(FixedConnection(parent=counterTop.root, child=sink_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-0.6, y=0, z=0.021)))

        # --- MODULE 1: Cabinet with swing door (60cm) ---
        m1_l = 0.60
        m1_x = -ct_l/2 + 0.30
        m1_body = Body(name=PrefixedName("ct_mod1_body"))
        m1_geom = ShapeCollection([Box(scale=Scale(m1_l, ct_d, ct_h), color=Color.GRAY())], reference_frame=m1_body)
        m1_geom.transform_all_shapes_to_own_frame()
        m1_body.collision, m1_body.visual = m1_geom, m1_geom
        world.add_connection(FixedConnection(parent=counterTop.root, child=m1_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=m1_x, z=-ct_h/2)))
        
        # Door for Mod 1 (Hinge Right, Handle Left - same as Fridge)
        m1_door_body = Body(name=PrefixedName("ct_mod1_door_body"))
        m1_door_geom = ShapeCollection([Box(scale=Scale(m1_l, 0.02, ct_h), color=Color.WHITE())], reference_frame=m1_door_body)
        m1_door_geom.transform_all_shapes_to_own_frame()
        m1_door_body.collision, m1_door_body.visual = m1_door_geom, m1_door_geom
        m1_hinge = Body(name=PrefixedName("ct_mod1_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=m1_body, child=m1_hinge,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-m1_l/2, y=ct_d/2, z=0),
            axis=Vector3.Z(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=np.pi/2))))
        world.add_connection(FixedConnection(parent=m1_hinge, child=m1_door_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=m1_l/2)))
        
        # Horizontal Handle for Mod 1
        m1_ha_body = Body(name=PrefixedName("ct_mod1_handle_body"))
        m1_ha_geom = ShapeCollection([Box(scale=Scale(m1_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=m1_ha_body)
        m1_ha_geom.transform_all_shapes_to_own_frame()
        m1_ha_body.collision, m1_ha_body.visual = m1_ha_geom, m1_ha_geom
        world.add_connection(FixedConnection(parent=m1_door_body, child=m1_ha_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=ct_h/3 - 0.05)))
        world.add_semantic_annotation(Door(root=m1_door_body, name=PrefixedName("ct_mod1_door")))

        # --- MODULE 2: Dishwasher (55cm) ---
        m2_l = 0.55
        m2_x = -ct_l/2 + 0.60 + 0.275
        m2_body = Body(name=PrefixedName("ct_mod2_body"))
        m2_geom = ShapeCollection([Box(scale=Scale(m2_l, ct_d, ct_h), color=Color.GRAY())], reference_frame=m2_body)
        m2_geom.transform_all_shapes_to_own_frame()
        m2_body.collision, m2_body.visual = m2_geom, m2_geom
        world.add_connection(FixedConnection(parent=counterTop.root, child=m2_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=m2_x, z=-ct_h/2)))
        
        # Dishwasher Door (Pull down)
        m2_door_body = Body(name=PrefixedName("ct_dw_door_body"))
        m2_door_geom = ShapeCollection([Box(scale=Scale(m2_l, 0.02, ct_h), color=Color.WHITE())], reference_frame=m2_door_body)
        m2_door_geom.transform_all_shapes_to_own_frame()
        m2_door_body.collision, m2_door_body.visual = m2_door_geom, m2_door_geom
        m2_hinge = Body(name=PrefixedName("ct_dw_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=m2_body, child=m2_hinge,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=ct_d/2, z=-ct_h/2),
            axis=Vector3.X(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=np.pi/2))))
        world.add_connection(FixedConnection(parent=m2_hinge, child=m2_door_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=ct_h/2)))
        
        # Dishwasher Handle
        m2_ha_body = Body(name=PrefixedName("ct_dw_handle_body"))
        m2_ha_geom = ShapeCollection([Box(scale=Scale(m2_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=m2_ha_body)
        m2_ha_geom.transform_all_shapes_to_own_frame()
        m2_ha_body.collision, m2_ha_body.visual = m2_ha_geom, m2_ha_geom
        world.add_connection(FixedConnection(parent=m2_door_body, child=m2_ha_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=ct_h/2 - 0.03)))
        world.add_semantic_annotation(Handle(root=m2_ha_body, name=PrefixedName("ct_dw_handle")))
        world.add_semantic_annotation(Door(root=m2_door_body, name=PrefixedName("ct_dishwasher_door")))

        # --- MODULE 3: 3 Drawers (89.4cm) ---
        m3_l = ct_l - m1_l - m2_l
        m3_x = ct_l/2 - m3_l/2
        m3_body = Body(name=PrefixedName("ct_mod3_body"))
        m3_geom = ShapeCollection([Box(scale=Scale(m3_l, ct_d, ct_h), color=Color.GRAY())], reference_frame=m3_body)
        m3_geom.transform_all_shapes_to_own_frame()
        m3_body.collision, m3_body.visual = m3_geom, m3_geom
        world.add_connection(FixedConnection(parent=counterTop.root, child=m3_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=m3_x, z=-ct_h/2)))
        
        # Drawer Heights: 40%, 40%, 20%
        h_bot, h_mid, h_top = ct_h * 0.4, ct_h * 0.4, ct_h * 0.2
        z_pos = [-ct_h/2 + h_bot/2, -ct_h/2 + h_bot + h_mid/2, ct_h/2 - h_top/2]
        h_list = [h_bot, h_mid, h_top]
        for i, (h, z) in enumerate(zip(h_list, z_pos)):
            dr_body = Body(name=PrefixedName(f"ct_drawer_{i}_body"))
            dr_front = ShapeCollection([Box(scale=Scale(m3_l, 0.02, h), color=Color.WHITE())], reference_frame=dr_body)
            dr_front.transform_all_shapes_to_own_frame()
            dr_body.collision, dr_body.visual = dr_front, dr_front
            world.add_connection(PrismaticConnection.create_with_dofs(world=world, parent=m3_body, child=dr_body,
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=ct_d/2, z=z),
                axis=Vector3.Y(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=0.4))))
            
            # Drawer Handles
            ha_body = Body(name=PrefixedName(f"ct_drawer_{i}_handle_body"))
            ha_geom = ShapeCollection([Box(scale=Scale(m3_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=ha_body)
            ha_geom.transform_all_shapes_to_own_frame()
            ha_body.collision, ha_body.visual = ha_geom, ha_geom
            world.add_connection(FixedConnection(parent=dr_body, child=ha_body, 
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=h/2 - 0.03)))
            world.add_semantic_annotation(Drawer(root=dr_body, name=PrefixedName(f"ct_drawer_{i}")))
        # --- OVEN TOWER (Modular Center + 2 Side Drawers) ---
        ot_l, ot_d, ot_h = 1.20, 0.658, 1.49
        ot_color = Color.GRAY()
        ot_root_T = root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=3.481, y=-2.181, z=ot_h)
        
        ovenTower = Cupboard.create_with_new_body_in_world(
            world=world, name=PrefixedName("oven_tower"),
            world_root_T_self=ot_root_T, scale=Scale(ot_l, ot_d, 0.04))
        for s in ovenTower.bodies[0].visual.shapes: s.color = ot_color

        m_center_l = 0.60
        m_side_l = (ot_l - m_center_l) / 2
        h_cabinet = 0.60
        h_drawer = 0.15
        h_oven = ot_h - h_cabinet - h_drawer

        # 1. Side Modules (Full-height Drawers)
        for side in [-1, 1]:
            s_n = "left" if side == -1 else "right"
            s_body = Body(name=PrefixedName(f"ot_side_{s_n}_body"))
            s_geom = ShapeCollection([Box(scale=Scale(m_side_l, ot_d, ot_h), color=Color.GRAY())], reference_frame=s_body)
            s_geom.transform_all_shapes_to_own_frame()
            s_body.collision, s_body.visual = s_geom, s_geom
            world.add_connection(FixedConnection(parent=ovenTower.root, child=s_body, 
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=side*(m_center_l/2 + m_side_l/2), z=-ot_h/2)))
            
            # Pull-out Drawer Front
            dr_body = Body(name=PrefixedName(f"ot_side_drawer_{s_n}_body"))
            dr_front = ShapeCollection([Box(scale=Scale(m_side_l, 0.02, ot_h), color=Color.WHITE())], reference_frame=dr_body)
            dr_front.transform_all_shapes_to_own_frame()
            dr_body.collision, dr_body.visual = dr_front, dr_front
            world.add_connection(PrismaticConnection.create_with_dofs(world=world, parent=s_body, child=dr_body,
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=ot_d/2),
                axis=Vector3.Y(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=0.4))))
            
            # Vertical Handle (4cm margin top/bottom)
            ha_body = Body(name=PrefixedName(f"ot_side_handle_{s_n}_body"))
            ha_geom = ShapeCollection([Box(scale=Scale(0.04, 0.02, ot_h - 0.08), color=Color.GRAY())], reference_frame=ha_body)
            ha_geom.transform_all_shapes_to_own_frame()
            ha_body.collision, ha_body.visual = ha_geom, ha_geom
            world.add_connection(FixedConnection(parent=dr_body, child=ha_body, 
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02)))
            world.add_semantic_annotation(Drawer(root=dr_body, name=PrefixedName(f"ot_side_drawer_{s_n}")))

        # 2. Center Section (Oven + Drawer + Cabinet)
        c_body = Body(name=PrefixedName("ot_center_body"))
        c_geom = ShapeCollection([Box(scale=Scale(m_center_l, ot_d, ot_h), color=Color.GRAY())], reference_frame=c_body)
        c_geom.transform_all_shapes_to_own_frame()
        c_body.collision, c_body.visual = c_geom, c_geom
        world.add_connection(FixedConnection(parent=ovenTower.root, child=c_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-ot_h/2)))

        # 2.1 Center Cabinet (Bottom)
        cab_body = Body(name=PrefixedName("ot_cab_body"))
        cab_front = ShapeCollection([Box(scale=Scale(m_center_l, 0.02, h_cabinet), color=Color.WHITE())], reference_frame=cab_body)
        cab_front.transform_all_shapes_to_own_frame()
        cab_body.collision, cab_body.visual = cab_front, cab_front
        cab_hinge = Body(name=PrefixedName("ot_cab_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=c_body, child=cab_hinge,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=m_center_l/2, y=ot_d/2, z=-ot_h/2 + h_cabinet/2),
            axis=Vector3.Z(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=np.pi/2))))
        world.add_connection(FixedConnection(parent=cab_hinge, child=cab_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=-m_center_l/2)))
        # Horizontal Handle for Cabinet
        ha_body = Body(name=PrefixedName("ot_cab_handle_body"))
        ha_geom = ShapeCollection([Box(scale=Scale(m_center_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=ha_body)
        ha_geom.transform_all_shapes_to_own_frame()
        ha_body.collision, ha_body.visual = ha_geom, ha_geom
        world.add_connection(FixedConnection(parent=cab_body, child=ha_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=h_cabinet/2 - 0.05)))
        world.add_semantic_annotation(Door(root=cab_body, name=PrefixedName("ot_cab_door")))

        # 2.2 Center Drawer (Middle)
        cdr_body = Body(name=PrefixedName("ot_center_drawer_body"))
        cdr_front = ShapeCollection([Box(scale=Scale(m_center_l, 0.02, h_drawer), color=Color.WHITE())], reference_frame=cdr_body)
        cdr_front.transform_all_shapes_to_own_frame()
        cdr_body.collision, cdr_body.visual = cdr_front, cdr_front
        world.add_connection(PrismaticConnection.create_with_dofs(world=world, parent=c_body, child=cdr_body,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=ot_d/2, z=-ot_h/2 + h_cabinet + h_drawer/2),
            axis=Vector3.Y(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=0.4))))
        # Handle for Drawer
        ha_body = Body(name=PrefixedName("ot_center_drawer_handle_body"))
        ha_geom = ShapeCollection([Box(scale=Scale(m_center_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=ha_body)
        ha_geom.transform_all_shapes_to_own_frame()
        ha_body.collision, ha_body.visual = ha_geom, ha_geom
        world.add_connection(FixedConnection(parent=cdr_body, child=ha_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=h_drawer/2 - 0.03)))
        world.add_semantic_annotation(Drawer(root=cdr_body, name=PrefixedName("ot_center_drawer")))

        # 2.3 Oven (Top)
        oven_door_body = Body(name=PrefixedName("ot_oven_door_body"))
        
        # White door frame
        oven_frame_geom = Box(scale=Scale(m_center_l, 0.02, h_oven), color=Color.WHITE())
        # Black glass panel
        oven_glass_geom = Box(scale=Scale(0.35, 0.005, 0.35), color=Color.BLACK())
        oven_glass_geom.origin = HomogeneousTransformationMatrix.from_xyz_rpy(y=0.011) # Slightly in front of white frame
        
        oven_door_geom = ShapeCollection([oven_frame_geom, oven_glass_geom], reference_frame=oven_door_body)
        oven_door_geom.transform_all_shapes_to_own_frame()
        oven_door_body.collision, oven_door_body.visual = oven_door_geom, oven_door_geom
        
        oven_hinge = Body(name=PrefixedName("ot_oven_hinge_body"))
        world.add_connection(RevoluteConnection.create_with_dofs(world=world, parent=c_body, child=oven_hinge,
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=ot_d/2, z=ot_h/2 - h_oven),
            axis=Vector3.X(), dof_limits=DegreeOfFreedomLimits(lower=DerivativeMap[float](position=0.0), upper=DerivativeMap[float](position=np.pi/2))))
        world.add_connection(FixedConnection(parent=oven_hinge, child=oven_door_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=h_oven/2)))
        # Handle for Oven
        ha_body = Body(name=PrefixedName("ot_oven_handle_body"))
        ha_geom = ShapeCollection([Box(scale=Scale(m_center_l - 0.06, 0.02, 0.03), color=Color.GRAY())], reference_frame=ha_body)
        ha_geom.transform_all_shapes_to_own_frame()
        ha_body.collision, ha_body.visual = ha_geom, ha_geom
        world.add_connection(FixedConnection(parent=oven_door_body, child=ha_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=0.02, z=h_oven/2 - 0.05)))
        world.add_semantic_annotation(Door(root=oven_door_body, name=PrefixedName("ot_oven_door")))


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

        # --- REFINED COFFEE TABLE (White, Front-Closed, with Floor) ---
        ct_l, ct_w, ct_h = 0.37, 0.91, 0.44
        ct_thick = 0.02
        ct_color = Color.WHITE()
        ct_root_T = root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=4.22, y=2.22, z=ct_h, yaw=np.pi)
        
        coffeeTable = Table.create_with_new_body_in_world(
            world=world, name=PrefixedName("coffee_table"),
            world_root_T_self=ct_root_T, scale=Scale(ct_l, ct_w, ct_thick))
        for s in coffeeTable.bodies[0].visual.shapes: s.color = ct_color

        # Middle Shelf
        shelf_body = Body(name=PrefixedName("coffee_table_shelf_body"))
        shelf_geom = ShapeCollection([Box(scale=Scale(ct_l, ct_w, 0.01), color=ct_color)], reference_frame=shelf_body)
        shelf_geom.transform_all_shapes_to_own_frame()
        shelf_body.collision, shelf_body.visual = shelf_geom, shelf_geom
        world.add_connection(FixedConnection(parent=coffeeTable.root, child=shelf_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-ct_h/2)))

        # Bottom Plate (Floor)
        floor_body = Body(name=PrefixedName("coffee_table_floor_body"))
        floor_geom = ShapeCollection([Box(scale=Scale(ct_l, ct_w, ct_thick), color=ct_color)], reference_frame=floor_body)
        floor_geom.transform_all_shapes_to_own_frame()
        floor_body.collision, floor_body.visual = floor_geom, floor_geom
        world.add_connection(FixedConnection(parent=coffeeTable.root, child=floor_body, 
            parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(z=-ct_h + ct_thick/2)))

        # Walls (Supporting structure) - Both short sides closed
        for i, y_dir in enumerate([-1, 1]):
            side_wall = Body(name=PrefixedName(f"coffee_table_wall_short_{i}_body"))
            side_wall_geom = ShapeCollection([Box(scale=Scale(ct_l, ct_thick, ct_h), color=ct_color)], reference_frame=side_wall)
            side_wall_geom.transform_all_shapes_to_own_frame()
            side_wall.collision, side_wall.visual = side_wall_geom, side_wall_geom
            world.add_connection(FixedConnection(parent=coffeeTable.root, child=side_wall, 
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(y=y_dir*(ct_w/2 - ct_thick/2), z=-ct_h/2)))

        # 2. Long Sides (1/3 closed at the front, 2/3 open at the back)
        wall_len = ct_w / 3
        for side in [-1, 1]:
            s_n = "left" if side == -1 else "right"
            long_wall_body = Body(name=PrefixedName(f"coffee_table_wall_long_{s_n}_body"))
            long_wall_geom = ShapeCollection([Box(scale=Scale(ct_thick, wall_len, ct_h), color=ct_color)], reference_frame=long_wall_body)
            long_wall_geom.transform_all_shapes_to_own_frame()
            long_wall_body.collision, long_wall_body.visual = long_wall_geom, long_wall_geom
            # Positioned at +y side (front)
            world.add_connection(FixedConnection(parent=coffeeTable.root, child=long_wall_body, 
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=side*(ct_l/2 - ct_thick/2), y=ct_w/2 - wall_len/2, z=-ct_h/2)))

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

        # Detailed White Desk Construction
        desk_l, desk_w, desk_h = 0.60, 1.20, 0.75
        desk_color = Color.WHITE()
        desk_plate_thick = 0.03
        
        desk = Desk.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("desk"),
            world_root_T_self=root_transformation @ HomogeneousTransformationMatrix.from_xyz_rpy(x=0.05, y=1.28, z=desk_h),
            scale=Scale(desk_l, desk_w, desk_plate_thick),
        )
        for shape in desk.root.visual.shapes: shape.color = desk_color

        leg_scale = Scale(0.04, 0.04, desk_h - desk_plate_thick)
        x_off = (desk_l / 2) - 0.02
        y_off = (desk_w / 2) - 0.02
        z_pos = -(desk_plate_thick / 2) - (leg_scale.z / 2)

        for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
            l_body = Body(name=PrefixedName(f"desk_leg_{i}_body"))
            l_geom = ShapeCollection([Box(scale=leg_scale, color=desk_color)], reference_frame=l_body)
            l_geom.transform_all_shapes_to_own_frame()
            l_body.collision, l_body.visual = l_geom, l_geom
            leg = Leg(root=l_body, name=PrefixedName(f"desk_leg_{i}"))
            world.add_connection(FixedConnection(
                parent=desk.root,
                child=l_body,
                parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=sx * x_off, y=sy * y_off, z=z_pos)
            ))
            world.add_semantic_annotation(leg)
            # desk.add_leg(leg) # Generic Desk might not have add_leg, using semantic annotation is enough

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
            for s in mod_cupboard.bodies[0].visual.shapes: s.color = Color.BEIGE()
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
