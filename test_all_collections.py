from pathlib import Path
import json
from typing import List, Dict

from test_collection import check_file

if __name__ == '__main__':
    json_data = Path(__file__, '..', 'language_resources.json').resolve()
    with json_data.open('r') as json_fp:
        data = json.load(json_fp)
        for language, resources in data.items():
            language: str
            resources: List[Dict[str, str]]
            for resource in resources:
                assert len(resource) == 1
                for resource_type, resource_file_path in resource.items():
                    if resource_type != 'pos':
                        resource_path = Path(resource_file_path).resolve()
                        check_file(resource_type, resource_path)
                    