import bpy
from mathutils import Vector

rows = 10  # Number of rows (y)
cols = 10  # Number of columns (x)
spacing = 2.0  # Distance between grid cells (world units)
period = 5  # Repeating period length (1 hole, then period-1 objects)
row_offset_step = (
    2  # How many columns to shift the pattern each subsequent row
)
start_offset = 0  # Initial horizontal offset in the period (0..period-1)
start_cell = (4, 4)  # Start stacking from this cell index (cx, cy)
use_linked_data = False  # True => instances share the same mesh data; False => meshes are copied
dest_collection_name = 'Stacked modules'
src_collection_name = 'Module'

if period < 1:
    raise ValueError('Period must be >= 1.')
if rows < 1 or cols < 1:
    raise ValueError('Rows and cols must be >= 1.')

# Find source collection
src_col = bpy.data.collections.get(src_collection_name)
if src_col is None:
    raise RuntimeError(f'Collection "{src_collection_name}" not found.')

# Create or get destination collection and ensure it's linked to the scene
dest_col = bpy.data.collections.get(dest_collection_name)
if dest_col is None:
    dest_col = bpy.data.collections.new(dest_collection_name)
    bpy.context.scene.collection.children.link(dest_col)
else:
    # Ensure linked to scene so items are visible
    if dest_col.name not in [
        c.name for c in bpy.context.scene.collection.children
    ]:
        bpy.context.scene.collection.children.link(dest_col)

# Clear destination collection (unlink its objects, then remove objects that are orphaned)
for o in list(dest_col.objects):
    try:
        dest_col.objects.unlink(o)
    except Exception:
        # Fallback: if unlink fails, ignore and continue
        pass
    # If object is not linked in any other collection, remove it from data
    if not o.users_collection:
        try:
            bpy.data.objects.remove(o, do_unlink=True)
        except Exception:
            pass


def cell_is_hole(row: int, col: int) -> bool:
    """Pattern rule: 1 == hole, 0 == place object"""
    row_offset = (start_offset + row * row_offset_step) % period
    return ((col - row_offset) % period) == 0


# Place
placed = 0
holes = 0

# Compute a cell-origin offset in world space:
# treat start_cell as cell indices, so world offset = (start_cell[0]*spacing, -start_cell[1]*spacing, 0)
base_cell_offset = Vector(
    (start_cell[0] * spacing, -start_cell[1] * spacing, 0.0)
)

for row in range(rows):
    for col in range(cols):
        if cell_is_hole(row, col):
            holes += 1
            continue

        # Compute this cell's world offset
        cell_origin = base_cell_offset + Vector(
            (col * spacing, -row * spacing, 0.0)
        )

        # Duplicate every object in the Module collection for this cell
        for src_obj in src_col.objects:
            new = src_obj.copy()
            # Copy mesh/data if requested (so each instance is editable independently)
            if src_obj.data is not None:
                if not use_linked_data:
                    try:
                        new.data = src_obj.data.copy()
                    except Exception:
                        # If copying fails, fallback to sharing data
                        new.data = src_obj.data
                else:
                    new.data = src_obj.data

            # Copy rotation/scale and rotation mode
            try:
                new.rotation_mode = src_obj.rotation_mode
                new.rotation_euler = src_obj.rotation_euler.copy()
            except Exception:
                pass
            try:
                new.rotation_quaternion = src_obj.rotation_quaternion.copy()
            except Exception:
                pass
            try:
                new.scale = src_obj.scale.copy()
            except Exception:
                pass

            # Place using the source local location plus the cell origin
            # (keeps relative object offsets inside the Module collection)
            new.location = src_obj.location + cell_origin

            # Give a helpful name
            new.name = f'{src_obj.name}_r{row}_c{col}'

            # Link into the destination collection
            dest_col.objects.link(new)
            placed += 1

print(
    f'Stacking done. Grid {rows}x{cols}, period={period}, step={row_offset_step}. Placed objects: {placed}, holes: {holes}.'
)
