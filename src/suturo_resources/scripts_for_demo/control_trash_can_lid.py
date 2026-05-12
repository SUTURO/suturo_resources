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
from semantic_digital_twin.world_description.connections import RevoluteConnection, FixedConnection
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_trash_can')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    lid_body = world.get_body_by_name(PrefixedName("trash_lid_body"))
    if not lid_body:
        print("Lid body not found")
        return
        
    conn_to_lid = lid_body.parent_connection
    hinge = None
    if isinstance(conn_to_lid, FixedConnection):
        hinge_body = conn_to_lid.parent
        hinge = hinge_body.parent_connection
    
    if isinstance(hinge, RevoluteConnection):
        print("Step 1: Opening trash can lid...")
        hinge.position = -np.pi/2
        viz.notify()
        time.sleep(2.0)
        
        print("Step 2: Closing trash can lid...")
        hinge.position = 0.0
        viz.notify()
        time.sleep(1.0)
    else:
        print("Hinge not found")
    
    rclpy.shutdown()

if __name__ == '__main__':
    run_showcase()
