from semantic_digital_twin.semantic_annotations.semantic_annotations import (
    Banana,
    Apple,
    Orange,
    Carrot,
    Lettuce,
    Table, Cup,
)
from semantic_digital_twin.world import World
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.spatial_types.spatial_types import (
    HomogeneousTransformationMatrix,
)
from semantic_digital_twin.world_description.world_entity import Body
from semantic_digital_twin.world_description.connections import (
    FixedConnection,
)
from semantic_digital_twin.world_description.geometry import (
    Box,
    Scale,
    Sphere,
    Cylinder,
    Color,
)
from semantic_digital_twin.world_description.shape_collection import ShapeCollection


def test_load_world():
    world = World()
    all_elements_connections = []
    root = Body(name=PrefixedName("root"))

    with world.modify_world():
        world.add_kinematic_structure_entity(root)
        fruit_table = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("fruit_table"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=0),
            scale=Scale(2, 2, 1),
        )

        vegetable_table = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("vegetable_table"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=2),
            scale=Scale(2, 2, 1),
        )

        empty_table = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("empty_table"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=4),
            scale=Scale(2, 2, 1),
        )

        empty_table2 = Table.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("empty_table2"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=6),
            scale=Scale(2, 2, 1),
        )


        apple = Apple.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("apple"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=0.55),
            scale=Scale(0.10, 0.10, 0.10),
        )
        for color in apple.bodies[0].visual.shapes:
            color.color = Color.RED()

        orange = Orange.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("orange"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=0.5, z=0.55),
            scale=Scale(0.10, 0.10, 0.10),
        )
        for color in orange.bodies[0].visual.shapes:
            color.color = Color.ORANGE()

        carrot = Carrot.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("carrot"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1, z=2.6),
            scale=Scale(0.05, 0.05, 0.20),
        )
        for color in carrot.bodies[0].visual.shapes:
            color.color = Color.ORANGE()

        lettuce = Lettuce.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("lettuce"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=1, y=1.5, z=2.55),
            scale=Scale(0.15, 0.15, 0.10),
        )
        for color in lettuce.bodies[0].visual.shapes:
            color.color = Color.GREEN()

        banana = Banana.create_with_new_body_in_world(
            world=world,
            name=PrefixedName("banana"),
            world_root_T_self=HomogeneousTransformationMatrix.from_xyz_rpy(x=10, y=10, z=10),
            scale=Scale(0.20, 0.05, 0.05),
        )
        for color in banana.bodies[0].visual.shapes:
            color.color = Color.YELLOW()


    toya = Cylinder(width=0.45, height=1.5)
    shape_geometry = ShapeCollection([toya])
    toya_body = Body(
        name=PrefixedName("base_link_body"),
        collision=shape_geometry,
        visual=shape_geometry,
    )

    root_C_toya = FixedConnection(
        parent=root,
        child=toya_body,
        parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(),
    )
    all_elements_connections.append(root_C_toya)


    with world.modify_world():
        for conn in all_elements_connections:
            world.add_connection(conn)

    return world
