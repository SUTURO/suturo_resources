from giskard_msgs.action import World
from krrood.entity_query_language.entity import variable, entity, contains
from krrood.entity_query_language.entity_result_processors import an
from krrood.entity_query_language.predicate import symbolic_function
from random_events.interval import Interval
from semantic_digital_twin.datastructures.variables import SpatialVariables
from semantic_digital_twin.reasoning.predicates import Below

from semantic_digital_twin.world_description.world_entity import Region, Body
from semantic_digital_twin.spatial_types import HomogeneousTransformationMatrix


from suturo_resources.suturo_map import load_environment


def query_region_area(world, region: str):
    """
    Queries an area from the environment.
    Returns the center of mass and global pose of a given region.
    """
    body = variable(type_=Region, domain=world.regions)
    query = an(entity(body).where(contains(body.name.name, region)))
    kitchen_room_area = list(query.evaluate())[0]
    return kitchen_room_area

def query_trash(world):
    """
    Queries the location of the trash can in the environment.
    Returns the x, y, z coordinates of the trash can's global pose.
    """
    body = variable(type_=Body, domain=world.bodies)
    query = an(entity(body).where(contains(body.name.name, "trash_can_body")))
    trash_can = list(query.evaluate())[0]
    return trash_can

def assign_distance_to_object(obj, pov):
    """
    Assigns a distance value to an object based on its position relative to a point of view (pov).
    :param obj: the object to calculate the distance for
    :param pov: ower point of view (robot) as [x, y]
    :return: the distance value as a float
    """
    dx = abs(obj.global_pose.x - pov[0])
    dy = abs(obj.global_pose.y - pov[1])
    dist_sq = dx + dy

    return float(dist_sq)

def eql_is_supported_by(support_body: Body):

    @symbolic_function
    def is_supported_by(
            supported_body: Body, supporting_body: Body, max_intersection_height: float = 0.1
    ) -> bool:
        """
        Checks if one object is supporting another object.

        :param supported_body: Object that is supported
        :param supporting_body: Object that potentially supports the first object
        :param max_intersection_height: Maximum height of the intersection between the two objects.
        If the intersection is higher than this value, the check returns False due to unhandled clipping.
        :return: True if the second object is supported by the first object, False otherwise
        """
        if supported_body == supporting_body:
            return False

        if supported_body.combined_mesh is None or supporting_body.combined_mesh is None:
            return False

        if Below(supported_body, supporting_body, supported_body.global_pose)():
            return False
        bounding_box_supported_body = (
            supported_body.collision.as_bounding_box_collection_at_origin(
                HomogeneousTransformationMatrix(reference_frame=supported_body)
            ).event
        )
        bounding_box_supporting_body = (
            supporting_body.collision.as_bounding_box_collection_at_origin(
                HomogeneousTransformationMatrix(reference_frame=supported_body)
            ).event
        )

        intersection = (
                bounding_box_supported_body & bounding_box_supporting_body
        ).bounding_box()

        if intersection.is_empty():
            return False

        z_intersection: Interval = intersection[SpatialVariables.z.value]
        size = sum([si.upper - si.lower for si in z_intersection.simple_sets])
        return size < max_intersection_height



    body = variable(Body, domain=support_body._world.bodies)
    results = list(
        an(entity(body).where(is_supported_by(supported_body=body, supporting_body=support_body)))
        .evaluate()
    )
    base_link_x = hsrb_world.get_kinematic_structure_entity_by_name(name="base_link").global_pose.to_position().x
    base_link_y = hsrb_world.get_kinematic_structure_entity_by_name(name="base_link").global_pose.to_position().y
    body2 = variable(Body, domain=results)
    results2_query = an(entity(body2).order_by(
        variable=body2, key=lambda b: assign_distance_to_object(b, HomogeneousTransformationMatrix.from_xyz_rpy(base_link_x, base_link_y)), descending=False
    ))

    print([b for b in list(results2_query.evaluate())])

# print(eql_is_supported_by(load_environment().get_body_by_name("base_link").global_pose.x))
# print(eql_is_supported_by(load_environment().get_body_by_name("cookingTable_body")))


def eql_is_supported_by2(support_body: Body, x: float, y: float):

    @symbolic_function
    def is_supported_by(
            supported_body: Body, supporting_body: Body, max_intersection_height: float = 0.1
    ) -> bool:
        """
        Checks if one object is supporting another object.

        :param supported_body: Object that is supported
        :param supporting_body: Object that potentially supports the first object
        :param max_intersection_height: Maximum height of the intersection between the two objects.
        If the intersection is higher than this value, the check returns False due to unhandled clipping.
        :return: True if the second object is supported by the first object, False otherwise
        """
        if supported_body == supporting_body:
            return False

        if supported_body.combined_mesh is None or supporting_body.combined_mesh is None:
            return False

        if Below(supported_body, supporting_body, supported_body.global_pose)():
            return False
        bounding_box_supported_body = (
            supported_body.collision.as_bounding_box_collection_at_origin(
                HomogeneousTransformationMatrix(reference_frame=supported_body)
            ).event
        )
        bounding_box_supporting_body = (
            supporting_body.collision.as_bounding_box_collection_at_origin(
                HomogeneousTransformationMatrix(reference_frame=supported_body)
            ).event
        )

        intersection = (
                bounding_box_supported_body & bounding_box_supporting_body
        ).bounding_box()

        if intersection.is_empty():
            return False

        z_intersection: Interval = intersection[SpatialVariables.z.value]
        size = sum([si.upper - si.lower for si in z_intersection.simple_sets])
        return size < max_intersection_height



    body = variable(Body, domain=support_body._world.bodies)
    results = list(
        an(entity(body).where(is_supported_by(supported_body=body, supporting_body=support_body)))
        .evaluate()
    )
    body2 = variable(Body, domain=results)
    results2_query = an(entity(body2).order_by(
        variable=body2, key=lambda b: assign_distance_to_object(b, HomogeneousTransformationMatrix.from_xyz_rpy(
            x, y)), descending=False
    ))

    print([b for b in list(results2_query.evaluate())])