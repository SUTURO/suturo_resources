from semantic_digital_twin.semantic_annotations.semantic_annotations import *
from semantic_digital_twin.world import World
from semantic_digital_twin.world_description.geometry import Color, Scale
from semantic_digital_twin.semantic_annotations.semantic_annotations import Sofa
import numpy as np

from conftest import test_load_world
from suturo_resources.queries import (
    query_surface_of_most_similar_obj,
    query_semantic_annotations_on_surfaces,
    query_get_next_object_euclidean_x_y, query_annotations_by_color, query_class_by_label, query_sort_by_size,
)
from suturo_resources.suturo_map import load_environment, Publisher


def test_load_environment_returns_world():
    """
    Tests that loading the environment returns a World object with the correct root name.
    """
    world = load_environment()
    publisher = Publisher("semantic_digital_twin")
    publisher.publish(world)
    assert isinstance(world, World)
    assert world.root.name == PrefixedName("root")


def test_sofa_structure():
    """
    Tests that the Sofa is correctly constructed with dimensions and color.
    """
    world = load_environment()
    sofas = world.get_semantic_annotations_by_type(Sofa)
    assert len(sofas) == 1
    sofa = sofas[0]

    # Check dimensions
    # Since the sofa is now a single body with complex geometry (CSG),
    # we check the bounding box of the entire object.
    # The expected dimensions correspond to the parameters from the factory:
    # scale=Scale(x=1.68, y=0.94, z=0.68)

    # Calculate the bounding box of all shapes combined in the local frame
    bbox = sofa.root.collision.as_bounding_box_collection_in_frame(sofa.root).bounding_box()

    # Tolerance for floating point numbers (numpy is required: import numpy as np)
    assert np.isclose(bbox.width, 0.94, atol=1e-3)  # x-axis (depth)
    assert np.isclose(bbox.depth, 1.68, atol=1e-3)  # y-axis (witdh)
    assert np.isclose(bbox.height, 0.68, atol=1e-3)  # z-axis (height)

    # Check color (Gray)
    # We check if shapes exist at all and if they have the correct color
    assert len(sofa.root.visual.shapes) > 0
    assert sofa.root.visual.shapes[0].color == Color.GRAY()

    # Check supporting surface
    assert sofa.supporting_surface is not None

def test_query_semantic_annotations_on_surfaces():
    """
    Tests that giving Table annotations gives a list of the correct annotation on top.
    """
    world = test_load_world()
    table1 = world.get_semantic_annotation_by_name("fruit_table")
    table2 = world.get_semantic_annotation_by_name("vegetable_table")
    table3 = world.get_semantic_annotation_by_name("empty_table")
    apple = world.get_semantic_annotation_by_name("apple")
    carrot = world.get_semantic_annotation_by_name("carrot")
    orange = world.get_semantic_annotation_by_name("orange")
    lettuce = world.get_semantic_annotation_by_name("lettuce")
    assert [type(x) for x in query_semantic_annotations_on_surfaces([table1, table2], world).evaluate()] == [type(x) for x in
        [apple,
        orange,
        carrot,
        lettuce,
    ]]
    assert set(query_semantic_annotations_on_surfaces([table3], world).tolist()) == set([])
    assert set(query_semantic_annotations_on_surfaces([], world).tolist()) == set([])


def test_query_get_next_object_euclidean_x_y():
    """
    Tests the functionality of the `query_get_next_object_euclidean_x_y` function to verify that it accurately identifies
    the next objects based on their Euclidean proximity within a simulation world. The test involves setting up a virtual
    world, retrieving specific objects and annotations, and validating the results returned by the function against
    predetermined expectations.

    :raises AssertionError: If any of the function assertions fail during testing.
    """
    world = test_load_world()
    toya = world.get_body_by_name("base_link_body")
    table1 = world.get_semantic_annotation_by_name("fruit_table")
    table2 = world.get_semantic_annotation_by_name("vegetable_table")
    table3 = world.get_semantic_annotation_by_name("empty_table")
    apple = world.get_semantic_annotation_by_name("apple")
    carrot = world.get_semantic_annotation_by_name("carrot")
    orange = world.get_semantic_annotation_by_name("orange")
    lettuce = world.get_semantic_annotation_by_name("lettuce")

    assert query_get_next_object_euclidean_x_y(toya, table1).tolist() == [orange, apple]
    assert query_get_next_object_euclidean_x_y(toya, table2).tolist() == [
        carrot,
        lettuce,
    ]
    assert query_get_next_object_euclidean_x_y(toya, table3).tolist() == []


def test_query_surface_of_most_similar_obj():
    """
    Tests the `query_surface_of_most_similar_obj` function for determining the surface of the most suitable
    semantic annotation object from a set of candidates based on similarity and
    other constraints. The function is evaluated under multiple scenarios to verify
    its logic in choosing the correct table, handling empty tables, and cases with
    no valid candidates.
    """
    world = test_load_world()
    table1 = world.get_semantic_annotation_by_name("fruit_table")
    table2 = world.get_semantic_annotation_by_name("vegetable_table")
    table3 = world.get_semantic_annotation_by_name("empty_table")
    table4 = world.get_semantic_annotation_by_name("empty_table2")

    banana = world.get_semantic_annotation_by_name("banana")
    apple = world.get_semantic_annotation_by_name("apple")
    carrot = world.get_semantic_annotation_by_name("carrot")
    orange = world.get_semantic_annotation_by_name("orange")
    lettuce = world.get_semantic_annotation_by_name("lettuce")

    # choosing the correct table
    assert query_surface_of_most_similar_obj(banana, [table1, table2, table3]) == table1
    assert query_surface_of_most_similar_obj(carrot, [table1, table2, table3]) == table2
    # choosing the empty table
    assert query_surface_of_most_similar_obj(lettuce, [table1, table3]) == table3
    assert query_surface_of_most_similar_obj(table1, [table1, table2, table3]) == table3
    # trying with a new threshold
    assert query_surface_of_most_similar_obj(orange, [table2, table3], 2) == table2
    # returning None if there is no empty table or no tables
    assert query_surface_of_most_similar_obj(apple, [table2]) == None
    assert query_surface_of_most_similar_obj(orange, []) == None
    # trying with 2 empty tables
    assert query_surface_of_most_similar_obj(apple, [table2, table3, table4]) == table3
    assert query_surface_of_most_similar_obj(apple, [table2, table4, table3]) == table4

def test_query_body_by_color():
    """
    Tests the query_annotations_by_color function by verifying the retrieval of semantic
    annotations by their associated colors.

    The function validates that calling query_annotations_by_color with different color
    parameters returns the expected list of annotations corresponding to that color
    within the given list of objects.
    """
    world = test_load_world()
    table1 = world.get_semantic_annotation_by_name("fruit_table")
    table2 = world.get_semantic_annotation_by_name("vegetable_table")
    apple = world.get_semantic_annotation_by_name("apple")
    orange = world.get_semantic_annotation_by_name("orange")
    carrot = world.get_semantic_annotation_by_name("carrot")

    assert query_annotations_by_color(Color.RED(), [apple, orange]) == [apple]
    assert query_annotations_by_color(Color.ORANGE(), [apple, orange]) == [orange]
    assert query_annotations_by_color(Color.BLUE(), [apple, orange,carrot]) == []
    assert query_annotations_by_color(Color.ORANGE(), (query_semantic_annotations_on_surfaces([table1, table2], world).tolist())) == [orange, carrot]

def test_query_class_by_label():
    """
    Tests the query_class_by_label function by verifying the retrieval of the semantic class
    """
    assert query_class_by_label("salt_aquasale_mill_transparent") == Salt
    assert query_class_by_label("milk_jumbo_pack_voll") == Milk
    assert query_class_by_label("bowl_collapsable_yellowgrey") == Bowl

    assert query_class_by_label("unknown_object") is None


def test_query_sort_by_size():
    """
    Tests the query_sort_by_size function by verifying the order of the returned annotations.
    """
    world = test_load_world()
    table1 = world.get_semantic_annotation_by_name("fruit_table")
    table2 = world.get_semantic_annotation_by_name("vegetable_table")

    apple = world.get_semantic_annotation_by_name("apple")
    carrot = world.get_semantic_annotation_by_name("carrot")
    lettuce = world.get_semantic_annotation_by_name("lettuce")

    assert query_sort_by_size([]) ==[]
    assert query_sort_by_size([apple, carrot]) == [apple, carrot]
    assert query_sort_by_size([table1, lettuce, apple]) == [table1, lettuce, apple]
    assert query_sort_by_size([table1, lettuce, apple], False) == [apple, lettuce, table1]
    assert query_sort_by_size(query_semantic_annotations_on_surfaces([table2], world).tolist()) == [lettuce, carrot]