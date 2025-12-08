#!/usr/bin/env python3

from cloudflare import CloudFlareR2


def upload_object_state_diagram(object_schema, cloudflare_r2):

    object_name_prefix = object_schema.object_name.lower().replace(' ', '-')
    state_diagram_filename = object_schema.state_diagram.filename
    state_diagram_r2_key = f'state-diagrams/{object_name_prefix}.png'

    print(f"Uploading state diagram for {object_name_prefix} from {state_diagram_filename} to R2 {state_diagram_r2_key}...")

    cloudflare_r2.upload_r2_object(state_diagram_filename, state_diagram_r2_key)


def upload_state_diagrams(object_schemas):

    print("Uploading state diagrams to R2...")
    cloudflare_r2 = CloudFlareR2()
    for object_schema in object_schemas:
        if object_schema.state_diagram:
            upload_object_state_diagram(object_schema, cloudflare_r2)
