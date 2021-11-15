from pathlib import Path
import json
from typing import List, Dict

from test_collection import check_file

if __name__ == '__main__':
    json_data = Path(__file__, '..', 'language_resources.json').resolve()
    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
        for _, meta_data in data.items():
            resources: List[Dict[str, str]] = meta_data['resources']
            for resource in resources:
                resource_type = resource['data type']
                resource_file_path = Path(resource['file path']).resolve()
                if resource_type != 'pos':
                    check_file(resource_type, resource_file_path)
                        
                    