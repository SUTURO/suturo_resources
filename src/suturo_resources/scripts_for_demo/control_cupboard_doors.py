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
    node = rclpy.create_node('showcase_cupboard_doors')
    world = load_environment()
    viz = VizMarkerPublisher(_world=world, node=node)
    viz.with_tf_publisher()
    
    # Geben wir der Visualisierung einen Moment Zeit zum Initialisieren
    time.sleep(1.0)
    
    # Alle Türen suchen
    doors = [d for d in world.get_semantic_annotations_by_type(Door) if d.name.name.startswith("cupboard_door")]
    
    print(f"Opening {len(doors)} Cupboard doors...")
    for door in doors:
        # Kinematik: door.root -> FixedConnection -> hinge_body -> RevoluteConnection
        door_body = door.root
        fixed_conn = door_body.parent_connection
        hinge_body = fixed_conn.parent
        revolute_conn = hinge_body.parent_connection
        
        # Position setzen
        target_pos = np.pi/2 if "left" in door.name.name else -np.pi/2
        print(f"Setting {door.name.name} to {target_pos}")
        revolute_conn.position = target_pos
    
    # Wichtig: Den World-Zustand explizit synchronisieren
    world.update_forward_kinematics()
    viz.notify()
    
    time.sleep(5.0)
    
    print("Closing Cupboard doors...")
    for door in doors:
        revolute_conn = door.root.parent_connection.parent.parent_connection
        revolute_conn.position = 0.0
        
    world.update_forward_kinematics()
    viz.notify()
    
    time.sleep(2.0)
    rclpy.shutdown()

if __name__ == '__main__': 
    run_showcase()
