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
from semantic_digital_twin.semantic_annotations.semantic_annotations import Door
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_ct_mod1_door')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    door = next((d for d in world.get_semantic_annotations_by_type(Door) if d.name.name == "ct_mod1_door"), None)
    
    # Kinematic chain: m1_anno.root -> m1_hinge -> m1_door_body
    # door.root is m1_door_body. Its parent connection is Fixed (to m1_hinge).
    # m1_hinge is parent of that Fixed connection.
    # m1_hinge's parent connection is the RevoluteConnection.
    fixed_conn = door.root.parent_connection
    hinge_body = fixed_conn.parent
    revolute_conn = hinge_body.parent_connection
    
    print("Opening CounterTop Module 1 Cabinet...")
    revolute_conn.position = np.pi/2
    viz.notify()
    time.sleep(2.0)
    
    revolute_conn.position = 0.0
    viz.notify()
    rclpy.shutdown()

if __name__ == '__main__': 
    run_showcase()
