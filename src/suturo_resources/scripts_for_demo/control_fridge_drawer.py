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
from semantic_digital_twin.world_description.connections import PrismaticConnection
from suturo_resources.suturo_map import load_environment
from semantic_digital_twin.adapters.ros.visualization.viz_marker import VizMarkerPublisher

def run_showcase():
    rclpy.init()
    node = rclpy.create_node('showcase_fridge_drawer')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    drawer = next((d for d in world.get_semantic_annotations_by_type(Drawer) if d.name.name == "fridge_drawer"), None)
    if not drawer:
        print("Fridge drawer not found")
        return
        
    slider = drawer.root.parent_connection
    
    if isinstance(slider, PrismaticConnection):
        print("Step 1: Opening fridge drawer...")
        slider.position = 0.4
        viz.notify()
        time.sleep(2.0)
        
        print("Step 2: Closing fridge drawer...")
        slider.position = 0.0
        viz.notify()
        time.sleep(1.0)
    else:
        print("Slider not found")
    
    rclpy.shutdown()

if __name__ == '__main__':
    run_showcase()
