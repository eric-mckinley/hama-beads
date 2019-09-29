# hama-beads
Raspberry Pi Project (Work in Progress)


### Steps

**Install PIL module**

For images -> `sudo pip install Pillow`

**Install requests module**

For http load -> `sudo pip install requests`

### Run Test

```bash
python -m unittest tests.test_pixel_image_parser
```

### Dry Run 

Local Image placing **reds** only

```bash
python hamapi/hama_beads_creator.py -t local -i test_resources/images/streetfighter_sagat.png
```

