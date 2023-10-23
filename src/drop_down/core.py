# -*- coding:utf-8 -*-
import bpy
import math
import mathutils

def get_bound_box_half_diagonal_vector(bound_box):
    return (mathutils.Vector(bound_box[6])-mathutils.Vector(bound_box[0]))*0.5

def get_bound_axis_point(bound_box, v_axis):
    bvc = get_bound_box_center(bound_box)
    bcv = get_bound_box_half_diagonal_vector(bound_box)
    ta = bcv.dot(v_axis)
    return bvc+v_axis*abs(ta)

def get_world_zd(obj):
    offd = ( obj.bound_box[1][2] - obj.bound_box[0][2] ) * 0.0001
    return obj.matrix_world@mathutils.Vector((0.0, 0.0, obj.bound_box[0][2]-offd)), obj.matrix_world@mathutils.Vector((0.0, 0.0, obj.bound_box[0][2]-1.0-offd))

def get_bound_box_diagonal_length(bound_box):
    return get_bound_box_half_diagonal_vector(bound_box).length*2

def get_bound_box_center(bound_box):
    return (mathutils.Vector(bound_box[6])-mathutils.Vector(bound_box[0]))*0.5+mathutils.Vector(bound_box[0])

def get_object_bound_box_center_length(obj1, obj2):
    obj1lc = mathutils.Vector(get_bound_box_center(obj1.bound_box))
    obj2lc = mathutils.Vector(get_bound_box_center(obj2.bound_box))
    return ((obj1.matrix_world@obj1lc)-(obj2.matrix_world@obj2lc)).length

def quaternion_from_p2p(v1, v2):
    return mathutils.Quaternion( v1.cross(v2), v1.angle(v2) )

def get_point_normal_align_transform(p1, n1, p2, n2):
    return quaternion_from_p2p(n1, n2), p2-p1

def matrix_transform_normal(m, v):
    t, r, s = m.decompose()
    return mathutils.Matrix.LocRotScale(None, r, s)@v

def test1():
    drop_action()

def drop_action():
    for each in bpy.data.objects[:]:
        if each.data is None:
            bpy.data.objects.remove(each)
    aobj = bpy.context.object
    sels = bpy.context.selected_objects
    if len(sels)<1:
        return
    elif len(sels) == 1:
        drop_one(aobj=None, robj=sels[0])
    drop_aobj = None
    if aobj in set(sels):
        drop_aobj = aobj
    for drop_robj in sels:
        if drop_robj is drop_aobj:
            continue
        drop_one(aobj=drop_aobj, robj=drop_robj)


def drop_one(aobj, robj):
    ov, dv = (get_world_zd(robj))
    # ov.xyz = [2, 0, 0]
    # dv.xyz = [-2, 0, 0]
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(ov))
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(dv))
    if aobj is None:
        res = bpy.context.scene.ray_cast(
            bpy.context.evaluated_depsgraph_get(),
            ov,
            dv-ov,
        )
    else:
        res = aobj.ray_cast(
            aobj.matrix_world.inverted()@ov,
            aobj.matrix_world.inverted()@dv-aobj.matrix_world.inverted()@ov,
        )
    print(res)
    if not res[0]:
        return
    if aobj is None:
        gd_point = res[1]
        gd_normal_point = res[1]+res[2]
    else:
        gd_point = aobj.matrix_world@(res[1])
        gd_normal_point = aobj.matrix_world@(res[1]+res[2])
    gd_normal = gd_normal_point - gd_point
    vup = mathutils.Vector((0, 0, 1))
    tv, rq, sv = robj.matrix_world.decompose()
    mm1 = mathutils.Matrix.Translation(get_bound_box_center(robj.bound_box)*-1.0)
    mm2 = mathutils.Matrix.Translation((0, 0, (robj.bound_box[1][2]-robj.bound_box[0][2])*0.5))
    rqcopy = rq.copy()
    vupproject = rq@vup
    rqm = mathutils.Quaternion( vupproject.cross(gd_normal), vupproject.angle(gd_normal) )
    rqcopy.rotate(rqm)
    mm3 = mathutils.Matrix.LocRotScale( None, rqcopy, sv )
    mm4 = mathutils.Matrix.Translation(gd_point)
    robj.matrix_world = mm4@mm3@mm2@mm1

    # for i, each in enumerate(bpy.context.object.bound_box):
    #     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(each))
    #     bpy.context.object.name = 'bound_box_p%s'%(i)
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(res[1]))
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(res[1]+res[2]))
    
    