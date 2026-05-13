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
from semantic_digital_twin.semantic_annotations.semantic_annotations import Drawer
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_ct_drawers')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    # Get all CounterTop drawers
    drawers = [d for d in world.get_semantic_annotations_by_type(Drawer) if d.name.name.startswith("ct_drawer_")]
    
    print(f"Opening {len(drawers)} CounterTop drawers...")
    for drawer in drawers:
        slider = drawer.root.parent_connection
        # Reduziert auf 0.25m, damit die 0.30m tiefen Schubladen nicht den Korpus verlassen
        slider.position = 0.25
    
    viz.notify()
    time.sleep(3.0)
    
    print("Closing CounterTop drawers...")
    for drawer in drawers:
        slider = drawer.root.parent_connection
        slider.position = 0.0
        
    viz.notify()
    time.sleep(2.0)
    rclpy.shutdown()

if __name__ == '__main__': 
    run_showcase()
