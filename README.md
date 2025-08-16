# robo-warehouse
## Idea for a robot-based architecture of a warehouse

[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/ebolblga/robo-warehouse/blob/master/README.md)
[![ru](https://img.shields.io/badge/lang-ru-red.svg)](https://github.com/ebolblga/robo-warehouse/blob/master/README.ru.md)
<!-- DeepWiki badge here: https://deepwiki.ryoppippi.com/ -->

<p align="center">
  <img src="assets/images/render.webp" alt="Warehouse render">
</p>

## Problem Statement
In fully automated warehouses where only robots operate, the traditional architecture with rows of racks and aisles between them is not always optimal. Modern approaches to designing such warehouses strive to maximize storage density, minimize space for robots to move, and increase overall efficiency.

My proposal is this tiling that uses **~80%** of total space for storage:

<p align="center">
  <img src="assets/images/tiling.webp" alt="Grid tiling">
</p>

Key idea is that you need to access any pallet without moving others, meaning that every pallet needs at least one face exposed, so it can be taken out.

The above shown grid tiling does exactly that, every pallet has one and exactly one air gap near it, and air gap is exactly the size of the pallet, so it can be extracted.

It is also worth noting that all pallets need to have fixed size for this to work (not neccessery squares). Thankfully there is a widely adopted standard size of a pallet: *EPAL pallet* 1.2m x 0.8m

## Possible implementation
Se we have the tiling, how would extraction and loading processes look like?

### Pallet extraction
Imagine a [scissor lift platform](https://en.wikipedia.org/wiki/Aerial_work_platform#:~:text=in%20their%20task.-,Scissor%20lift,-%5Bedit%5D) on a [roomba](https://en.wikipedia.org/wiki/Roomba) - this is the base of a robot, that could operate on such storage. They have planty of splace under the shelves to move around with the pallets and a simple A* algorightm with collision constaints should do the job for logistics of moving around.

Pallets themselves should be on rollers and slightly angled towards the hole as shown below (you would need some small lock mechanism, so they don't just slide down):

<p align="center">
  <img src="assets/images/extraction_example.webp" alt="Pallet extraction example">
</p>

Now taking a pallet out is as simple as lifting the platform in the needed hole and unlocking the needed pallet, it will roll down on the platform.

### Pallet loading
Loading operation is pretty similar to extraction. That scissor lift platform should have it's own rollers on the top. Now you simply move push the box in it's section and lock the mechanism to stop it from rolling back. No manipulator hands needed!

<p align="center">
  <img src="assets/images/loading_example.webp" alt="Pallet loading example">
</p>

## Renders
I made a simple Python script `src/main.py` for [Blender](https://www.blender.org/) thats takes specified collection and stacks it up according to the tiling pattern.

Then made a low-polly low-effort module just for demonstation. Then I did some kitbashing with external assets:
- [Wooden pallet](https://skfb.ly/oUrRI) by *Mehdi Shahsavan* from Sketchfab (CC Attribution license)
- [Cardboard box](https://skfb.ly/o9SFu) by *PolyProps3D* from Sketchfab (CC Attribution license)
- [Empty wokrshop HDRI](https://polyhaven.com/a/empty_workshop) by *Sergej Majboroda* from Poly Haven (CC0 license)

After running the script it will do the following:

<p align="center">
  <img src="assets/images/blender_viewport.webp" alt="Blender viewport">
</p>

## Conclusion
I am not familiar with the problematics of warehouses and their logistics. But this seems like a viable option to me.

## Setup with [Python](https://www.python.org/downloads/)
```bash
# Install the UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" on Windows

# Clone the repository and navigate into it
git clone https://github.com/ebolblga/robo-warehouse.git
cd robo-warehouse

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
. .venv/bin/activate
# .venv\Scripts\activate on Windows

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit
uv run pre-commit run --all-files

# Ruff
uv run ruff format
uv run ruff check --fix
```

## [License](https://github.com/ebolblga/robo-warehouse/blob/master/LICENSE.md)
This program is licensed under the MIT License. Please read the License file to know about the usage terms and conditions.
