import sys
import random_events.utils
try:
    import krrood.utils
    import krrood.adapters.json_serializer
    random_events.utils.recursive_subclasses = krrood.utils.recursive_subclasses
    random_events.utils.SubclassJSONSerializer = krrood.adapters.json_serializer.SubclassJSONSerializer
except ImportError:
    def recursive_subclasses(cls):
        return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in recursive_subclasses(s)]
    random_events.utils.recursive_subclasses = getattr(random_events.utils, 'recursive_subclasses', recursive_subclasses)

import rclpy
import time
import numpy as np
from semantic_digital_twin.world import World
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.semantic_annotations.semantic_annotations import Door, Drawer
from semantic_digital_twin.world_description.connections import RevoluteConnection, PrismaticConnection, FixedConnection
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_oven_door')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    door = next((d for d in world.get_semantic_annotations_by_type(Door) if d.name.name == "ot_oven_door"), None)
    hinge = door.root.parent_connection
    print("Opening oven...")
    hinge.position = np.pi/2
    viz.notify()
    time.sleep(2.0)
    hinge.position = 0.0
    viz.notify()
    rclpy.shutdown()
if __name__ == '__main__': run_showcase()
