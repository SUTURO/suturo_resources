import math
from typing import List, Union, Optional
#from entity_query_language.symbolic import QueryObjectDescriptor
from krrood.entity_query_language.factories import variable_from, entity, flat_variable, in_, the, contains, not_
from krrood.entity_query_language.query.query import Entity
from krrood.entity_query_language.predicate import symbolic_function
from krrood.utils import inheritance_path_length, recursive_subclasses
from semantic_digital_twin.reasoning.predicates import (
    is_supported_by,
    compute_euclidean_distance_2d,
    is_supporting,
)
from semantic_digital_twin.semantic_annotations.mixins import HasSupportingSurface, IsPerceivable
from semantic_digital_twin.semantic_annotations.semantic_annotations import Fruit, Food, Apple, Carrot, Banana
from semantic_digital_twin.world import World
#from semantic_digital_twin.semantic_annotations.mixins import HasDestination
from semantic_digital_twin.world_description.geometry import Color

from semantic_digital_twin.world_description.world_entity import (
    Body,
    SemanticAnnotation,
)

from conftest import test_load_world


def query_semantic_annotations_on_surfaces(
    supporting_surfaces: List[SemanticAnnotation], world: World
) -> Union[Entity[SemanticAnnotation], SemanticAnnotation]:
    """
    Queries a list of Semantic annotations that are on top of a given list of other annotations (ex. Tables).
    param: supporting_surfaces: List of SemanticAnnotations that are supporting other annotations.
    :param world: World object that contains the supporting_surfaces.
    return: List of SemanticAnnotations that are supported by the given supporting_surfaces.
    """
    supporting_surfaces_var = variable_from(supporting_surfaces)
    body_with_enabled_collision = variable_from(world.bodies_with_enabled_collision)
    semantic_annotations = flat_variable(
        body_with_enabled_collision._semantic_annotations
    )
    semantic_annotations_that_are_supported = entity(semantic_annotations).where(
        is_supported_by(
            supported_body=body_with_enabled_collision,
            supporting_body=supporting_surfaces_var.bodies[0],
        )
    )
    return semantic_annotations_that_are_supported


def query_get_next_object_euclidean_x_y(
    main_body: Body,
    supporting_surface,
) -> Entity[SemanticAnnotation]:
    """
    Queries the next object based on Euclidean distance in x and y coordinates
    relative to the given main body and supporting surface. This function utilizes
    semantic annotations of objects and orders them by their Euclidean distances
    to the main body.

    :param main_body: The main body to which the Euclidean distance is computed.
    :param supporting_surface: The surface on which the semantic annotations
        of interest are queried.
    :return: A `QueryObjectDescriptor` containing semantic annotations ordered
        by Euclidean distance to the main body.
    """
    supported_semantic_annotations = query_semantic_annotations_on_surfaces(
        [supporting_surface], main_body._world
    )
    return supported_semantic_annotations.ordered_by(
        compute_euclidean_distance_2d(
            body1=supported_semantic_annotations.selected_variable.bodies[0],
            body2=main_body,
        )
    )


def query_surface_of_most_similar_obj(
    object_of_interest: SemanticAnnotation,
    supporting_surfaces: List[HasSupportingSurface],
    threshold: int = 1,
) -> Optional[HasSupportingSurface]:
    """
    Finds the most similar object to a given semantic annotation among a list of tables
    based on the inheritance path length. If the similarity does not meet the provided
    threshold, the method attempts to return the table that is not supporting any object.
    The similarity metric leverages the class hierarchy to compute distances.

    :param object_of_interest: The semantic annotation to compare.
    :param supporting_surfaces: A list of supporting surfaces semantic annotations to search on top of them for similar objects to the object_of_interest.
    :param threshold: The maximum acceptable inheritance path length to classify objects
                      as similar. Defaults to 1.
    :return: The semantic annotation of the most appropriate surface based on similarity
             metrics or the non-supporting table when no viable candidate is found, or None if there are no supporting surfaces.
    """
    if not supporting_surfaces:
        return None

    # Find the surface that is not supporting anything
    non_supporting_table = None
    for supporting_surface in supporting_surfaces:
        if not is_supporting(supporting_surface.bodies[0]):
            non_supporting_table = supporting_surface
            break

    # Query annotations on the surfaces of the tables
    objects = query_semantic_annotations_on_surfaces(
        supporting_surfaces, object_of_interest._world
    ).tolist()

    best_distance = math.inf
    most_similar = None

    # Iterate over each object to find the most similar based on inheritance path length
    for obj in objects:
        for cls in type(obj).__mro__:
            dist = inheritance_path_length(type(object_of_interest), cls)
            if dist is None:
                continue
            if dist < best_distance:
                best_distance = dist
                most_similar = obj
            break  # Once a match is found, no need to check further classes for this object

    # Apply threshold to determine if the match is acceptable
    if best_distance > threshold or most_similar is None:
        return non_supporting_table

    # Find the table supporting the most similar object
    for supporting_surface in supporting_surfaces:
        if is_supported_by(most_similar.bodies[0], supporting_surface.bodies[0]):
            return supporting_surface

@symbolic_function
def compute_min_inheritance_distance(obj: SemanticAnnotation, target_type: type) -> float:
    """
    Compute the minimum inheritance path length between an object and a target type.
    Returns infinity if no inheritance path exists.
    """
    best_distance = math.inf
    for cls in type(obj).__mro__:
        dist = inheritance_path_length(target_type, cls)
        if dist is not None and dist < best_distance:
            best_distance = dist
            break
    return best_distance


def query_surface_of_most_similar_obj_eql(
    object_of_interest: SemanticAnnotation,
    supporting_surfaces: List[HasSupportingSurface],
    threshold: int = 1,
) -> Optional[HasSupportingSurface]:
    """
    EQL-based version: Finds the most similar object to a given semantic annotation among a list of tables
    based on the inheritance path length. If the similarity does not meet the provided
    threshold, the method attempts to return the table that is not supporting any object.
    The similarity metric leverages the class hierarchy to compute distances.

    :param object_of_interest: The semantic annotation to compare.
    :param supporting_surfaces: A list of supporting surfaces semantic annotations to search on top of them for similar objects to the object_of_interest.
    :param threshold: The maximum acceptable inheritance path length to classify objects
                      as similar. Defaults to 1.
    :return: The semantic annotation of the most appropriate surface based on similarity
             metrics or the non-supporting table when no viable candidate is found, or None if there are no supporting surfaces.
    """
    if not supporting_surfaces:
        return None

    # Find the surface that is not supporting anything using EQL
    supporting_surfaces_var = variable_from(supporting_surfaces)
    non_supporting_surface = entity(supporting_surfaces_var).where(
        not_(is_supporting(supporting_surfaces_var.bodies[0]))
    )
    non_supporting_table = non_supporting_surface.first() if non_supporting_surface.tolist() else None

    # Query annotations on the surfaces using EQL
    objects = query_semantic_annotations_on_surfaces(
        supporting_surfaces, object_of_interest._world
    )

    # Order objects by inheritance distance and get the most similar
    objects_ordered_by_similarity_list = objects.ordered_by(
        compute_min_inheritance_distance(objects.selected_variable, type(object_of_interest))
    ).tolist()

    if not objects_ordered_by_similarity_list:
        return non_supporting_table

    most_similar = objects_ordered_by_similarity_list[0]

    # Apply threshold to determine if the match is acceptable
    best_distance = compute_min_inheritance_distance(most_similar, type(object_of_interest))
    if best_distance > threshold:
        return non_supporting_table

    # Find the table supporting the most similar object using EQL
    most_similar_body = most_similar.bodies[0]
    supporting_surface_result = entity(supporting_surfaces_var).where(
        is_supported_by(most_similar_body, supporting_surfaces_var.bodies[0])
    )

    return supporting_surface_result.first()


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




def query_annotations_by_color(color: Color, objects: list[SemanticAnnotation]) -> List[SemanticAnnotation]:
    """
    Queries and retrieves a list of annotations from another one that match
    the specified color based on their visual properties.

    :param color: The color to filter annotations by.
    :param objects: The list of the unfiltered annotations.

    :return: List[SemanticAnnotation]: A list of annotations from the world whose primary shape's
    visual color matches the specified color.
    """
    all_bodies = []
    for obj in objects:
        all_bodies.append(obj.bodies[0])

    filtered_bodies = []

    for body in all_bodies:
        if body.visual and body.collision is None:
            continue
        shapes = body.visual.shapes or body.collision.shapes
        if shapes[0].color == color:
            filtered_bodies.append(body)
    filtered_annotations = []
    for body in filtered_bodies:
        filtered_annotations.append(list(body._semantic_annotations)[0])
    return filtered_annotations


@symbolic_function
def class_name_in_label(cls: type, label: str) -> bool:
    """Check if the class name is contained in the label."""
    return cls.__name__.lower() in label.lower()


def query_class_by_label(label: str) -> Optional[type]:
    """
    Finds the class whose name is contained within the given label.
    It searches through all subclasses of IsPerceivable.

    :param label: The string input from perception (e.g., "bowl_collapsable_yellowgrey").
    :return: The matching class (e.g., Bowl) or None if no match is found.
    """
    semantic_class = variable_from(recursive_subclasses(IsPerceivable))
    matching_class = entity(semantic_class).where(
        class_name_in_label(semantic_class, label)
    )
    return None if matching_class.tolist() == [] else matching_class.first()


# def query_object_destination(world: World, obj: HasDestination) -> List[SemanticAnnotation]:
#     """
#     Query suitable destination semantic annotations for a given object.
#
#     The object's class defines one or multiple preferred destination types via
#     the `destination_class_names` class variable.
#
#     :param world: The world containing semantic annotations.
#     :param obj: The object to be brought somewhere (must support HasDestination).
#     :return: A list of all destination semantic annotations found in the world.
#              The list may be empty.
#     """
#     dest_types = obj.destination_class_names
#
#     if not dest_types:
#         return []
#
#     # Result
#     results: List[SemanticAnnotation] = []
#     for dest_type in dest_types:
#         results.extend(world.get_semantic_annotations_by_type(dest_type))
#     return results

@symbolic_function
def get_object_mro(obj: SemanticAnnotation) -> tuple:
    """
    Returns the Method Resolution Order (MRO) of the object's type.
    """
    return type(obj).__mro__

@symbolic_function
def get_inheritance_distance(target_type: type, cls: type) -> float:
    """
    Get the inheritance path length between target_type and cls.
    Returns infinity if no inheritance path exists.
    """
    dist = inheritance_path_length(target_type, cls)
    return dist if dist is not None else math.inf


def query_surface_of_most_similar_obj_eql1(
    object_of_interest: SemanticAnnotation,
    supporting_surfaces: List[HasSupportingSurface],
    threshold: int = 1,
) -> Optional[HasSupportingSurface]:
    """
    EQL-based version: Finds the most similar object to a given semantic annotation among a list of tables
    based on the inheritance path length. If the similarity does not meet the provided
    threshold, the method attempts to return the table that is not supporting any object.
    The similarity metric leverages the class hierarchy to compute distances.

    :param object_of_interest: The semantic annotation to compare.
    :param supporting_surfaces: A list of supporting surfaces semantic annotations to search on top of them for similar objects to the object_of_interest.
    :param threshold: The maximum acceptable inheritance path length to classify objects
                      as similar. Defaults to 1.
    :return: The semantic annotation of the most appropriate surface based on similarity
             metrics or the non-supporting table when no viable candidate is found, or None if there are no supporting surfaces.
    """
    if not supporting_surfaces:
        return None

    # Find the surface that is not supporting anything using EQL
    supporting_surfaces_var = variable_from(supporting_surfaces)
    non_supporting_surface = entity(supporting_surfaces_var).where(
        not_(is_supporting(supporting_surfaces_var.bodies[0]))
    )
    non_supporting_table = non_supporting_surface.first() if non_supporting_surface.tolist() else None

    # Query annotations on the surfaces using EQL
    objects = query_semantic_annotations_on_surfaces(
        supporting_surfaces, object_of_interest._world
    )

    # Get MRO for each object and compute minimum distance using EQL (replaces compute_min_inheritance_distance1)
    mro = flat_variable(get_object_mro(objects.selected_variable))

    # Order objects by minimum inheritance distance - EQL handles the iteration over MRO classes
    objects_ordered_by_similarity_list = objects.ordered_by(
        the(entity(mro).ordered_by(
            get_inheritance_distance(type(object_of_interest), mro)
        ))
    ).tolist()

    if not objects_ordered_by_similarity_list:
        return non_supporting_table

    most_similar = objects_ordered_by_similarity_list[0]

    # Apply threshold - compute minimum distance using EQL (replaces compute_min_inheritance_distance1)
    mro_similar = flat_variable(get_object_mro(most_similar))
    best_distance_cls = entity(mro_similar).ordered_by(
        get_inheritance_distance(type(object_of_interest), mro_similar)
    ).first()
    best_distance_value = get_inheritance_distance(type(object_of_interest), best_distance_cls)

    if best_distance_value > threshold:
        return non_supporting_table

    # Find the table supporting the most similar object using EQL
    most_similar_body = most_similar.bodies[0]
    supporting_surface_result = entity(supporting_surfaces_var).where(
        is_supported_by(most_similar_body, supporting_surfaces_var.bodies[0])
    )

    return supporting_surface_result.first()