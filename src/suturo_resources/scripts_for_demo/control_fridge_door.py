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
from semantic_digital_twin.world_description.connections import RevoluteConnection, FixedConnection
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_fridge_door')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    fridge_door = next((d for d in world.get_semantic_annotations_by_type(Door) if d.name.name == "fridge_door"), None)
    if not fridge_door:
        print("Fridge door not found")
        return

    # Door root -> FixedConnection -> hinge_body -> RevoluteConnection -> frame_body
    conn_to_door = fridge_door.root.parent_connection
    hinge = None
    if isinstance(conn_to_door, FixedConnection):
        hinge_body = conn_to_door.parent
        hinge = hinge_body.parent_connection
    
    if isinstance(hinge, RevoluteConnection):
        print("Step 1: Opening fridge door...")
        hinge.position = -1.57
        viz.notify() # Update RViz
        time.sleep(2.0)
        
        print("Step 2: Closing fridge door...")
        hinge.position = 0.0
        viz.notify() # Update RViz
        time.sleep(1.0)
    else:
        print("Hinge not found")
    
    rclpy.shutdown()

if __name__ == '__main__':
    run_showcase()
