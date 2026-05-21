# from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
# from semantic_digital_twin.world import World
# from semantic_digital_twin.semantic_annotations.semantic_annotations import (
#     Milk,
#     Fridge,
#     Cup,
#     Cupboard,
#     Sink,
#     Bottle,
#     Table,
# )
# from suturo_resources.queries import query_object_destination
# from semantic_digital_twin.world_description.geometry import Scale
# from semantic_digital_twin.world_description.world_entity import Body
#
#
# def test_milk_goes_to_fridge():
#     world = World(name="test_world")
#
#     # Create root Body with name
#     root = Body(name=PrefixedName("root"))
#     with world.modify_world():
#         world.add_body(root)
#         fridge = Fridge.create_with_new_body_in_world(
#             name=PrefixedName("fridge"),
#             world=world,
#             scale=Scale(1.0, 1.0, 2.0),
#         )
#         milk = Milk.create_with_new_body_in_world(
#             name=PrefixedName("milk"),
#             world=world,
#             scale=Scale(0.1, 0.1, 0.2),
#         )
#
#     targets = query_object_destination(world, milk)
#     assert fridge in targets
#     assert len(targets) == 1
#
#
# def test_cup_goes_to_cupboard_table_sink():
#     world = World(name="test_world")
#
#     # Create root Body with name
#     root = Body(name=PrefixedName("root"))
#     with world.modify_world():
#         world.add_body(root)
#         cupboard = Cupboard.create_with_new_body_in_world(
#             name=PrefixedName("cupboard"),
#             world=world,
#             scale=Scale(0.8, 0.8, 1.8),
#         )
#         table = Table.create_with_new_body_in_world(
#             name=PrefixedName("table"),
#             world=world,
#             scale=Scale(1.0, 1.0, 0.1),
#         )
#         sink = Sink.create_with_new_body_in_world(
#             name=PrefixedName("sink"),
#             world=world,
#             scale=Scale(0.8, 0.6, 0.2),
#         )
#         cup = Cup.create_with_new_body_in_world(
#             name=PrefixedName("cup"),
#             world=world,
#             scale=Scale(0.05, 0.05, 0.08),
#         )
#
#     assert getattr(type(cup), "destination_class_names", None), "Class list Cup empty?"
#
#
#     targets = query_object_destination(world, cup)
#     assert cupboard in targets
#     assert table in targets
#     assert sink in targets
#     assert len(targets) == 3
#
#
# def test_bottle_goes_to_sink_cupboard():
#     world = World(name="test_world")
#
#     # Create root Body with name
#     root = Body(name=PrefixedName("root"))
#     with world.modify_world():
#         world.add_body(root)
#         sink = Sink.create_with_new_body_in_world(
#             name=PrefixedName("sink"),
#             world=world,
#             scale=Scale(0.8, 0.6, 0.2),
#         )
#         cupboard = Cupboard.create_with_new_body_in_world(
#             name=PrefixedName("cupboard"),
#             world=world,
#             scale=Scale(0.8, 0.8, 1.8),
#         )
#         bottle = Bottle.create_with_new_body_in_world(
#             name=PrefixedName("bottle"),
#             world=world,
#             scale=Scale(0.05, 0.05, 0.2),
#         )
#
#
#     targets = query_object_destination(world, bottle)
#     assert sink in targets
#     assert cupboard in targets
#     assert len(targets) == 2