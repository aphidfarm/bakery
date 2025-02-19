import bpy

C = bpy.context
D = bpy.data

bl_info = {
    "name": "Bakery",
    "description": "Bakery",
    "version": (0, 1),
    "blender": (4, 3, 0),
    "category": "Material"
}

class BakerySettings(bpy.types.PropertyGroup):
    color:      bpy.props.BoolProperty(name="color",    default = True)
    normal:     bpy.props.BoolProperty(name="normal",   default = True)
    rough:      bpy.props.BoolProperty(name="rough",    default = True)
    metal:      bpy.props.BoolProperty(name="metal",    default = False)
    emissive:   bpy.props.BoolProperty(name="emissive", default = False)
    alpha:      bpy.props.BoolProperty(name="alpha",    default = False)

    bake_name:  bpy.props.StringProperty(name="bake_name", default = "bake")
    image_size: bpy.props.EnumProperty(name="image_size", items=[("1024", "1024x1024", "1024x1024"), ("2048", "2048x2048", "2048x2048"), ("4096", "4096x4096", "4096x4096"), ("8192", "8192x8192", "8192x8192")], default = "1024")

class BakePrep(bpy.types.Operator):
    """Prepare baking resources. Adds a UV map and creates images for each selected map."""
    bl_idname = "material.bake_prep"
    bl_label = "Prep Bake Resources"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.object:
            return {'CANCELLED'}

        if "Bake" not in context.object.data.uv_layers.keys():
            context.object.data.uv_layers.new(name="Bake")

        images = []
        settings = context.scene.bakerysettings
        if (settings.color):
            images.append("_color")
        if (settings.normal):
            images.append("_normal")
        if (settings.rough):
            images.append("_rough")
        if (settings.metal):
            images.append("_metal")
        if (settings.emissive):
            images.append("_emissive")
        if (settings.alpha):
            images.append("_alpha")

        for i in images:
            if not i in D.images.keys():
                bpy.ops.image.new(
                    name=settings.bake_name + i,
                    width=int(settings.image_size),
                    height=int(settings.image_size),
                    color=(0, 0, 0, 1),
                    alpha=False,
                    generated_type='BLANK',
                    float=False,
                    use_stereo_3d=False,
                    tiled=False
                )

        return {'FINISHED'}

class BakeClear(bpy.types.Operator):
    """Clear prepared baking resources. Removes image texture nodes. Does not delete images."""
    bl_idname = "material.bake_clear"
    bl_label = "Clear Bake Resources"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not C.object:
            return {'CANCELLED'}

        for mat in D.materials:
            if mat.use_nodes == False:
                continue
            for node in mat.node_tree.nodes:
                if node.name == "Bake Texture":
                    mat.node_tree.nodes.remove(node)
        return {'FINISHED'}

class BakePanel(bpy.types.Panel):
    """Bake Panel"""
    bl_label       = "Bakery"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Bakery"

    def draw(self, context):
        self.layout.operator(BakePrep.bl_idname, text="Prep Bake Resources", icon = "UV_DATA")
        box = self.layout.box()
        box.label(text="Texture name prefix")
        box.prop(context.scene.bakerysettings, "bake_name", text="");

class BakePanelMapSettings(bpy.types.Panel):
    """Bake Panel Map Settings"""
    bl_label       = "Map Settings"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Bakery"
    bl_parent_id   = "BakePanel"

    def draw(self, context):
        self.layout.prop(context.scene.bakerysettings, "image_size", text="");
        row = self.layout.row(align=True)
        row.prop(context.scene.bakerysettings, "color",    text="Color Map",     toggle=True, invert_checkbox=False);
        row.prop(context.scene.bakerysettings, "normal",   text="Normal Map",    toggle=True, invert_checkbox=False);
        row = self.layout.row(align=True)
        row.prop(context.scene.bakerysettings, "rough",    text="Roughness Map", toggle=True, invert_checkbox=False);
        row.prop(context.scene.bakerysettings, "metal",    text="Metal Map",     toggle=True, invert_checkbox=False);
        row = self.layout.row(align=True)
        row.prop(context.scene.bakerysettings, "emissive", text="Emissive Map",  toggle=True, invert_checkbox=False);
        row.prop(context.scene.bakerysettings, "alpha",    text="Alpha Map",     toggle=True, invert_checkbox=False);
        row = self.layout.row(align=True)

class CleanPanel(bpy.types.Panel):
    """Clean Panel"""
    bl_label       = "Clean Up"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Bakery"

    def draw(self, context):
        self.layout.operator(BakeClear.bl_idname, text="Clear Bake Resources", icon = "TRASH")

classes = (
    BakePrep,
    BakeClear,
    BakePanel,
    CleanPanel,
    BakerySettings,
    BakePanelMapSettings
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.bakerysettings = bpy.props.PointerProperty(type=BakerySettings)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.bakerysettings

if __name__ == "__main__":
    register()
