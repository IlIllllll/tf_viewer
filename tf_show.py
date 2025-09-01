# 在 Jupyter 里先运行（推荐）
# %matplotlib widget  # 想要更丝滑的交互可启用此行

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as w
from pytransform3d.plot_utils import make_3d_axis
from pytransform3d.transformations import plot_transform, transform_from
from pytransform3d.rotations import matrix_from_euler

# 画布和坐标轴
ax = make_3d_axis(ax_s=1.0)
ax.set_title("Interactive Pose: xyz + roll/pitch/yaw")
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)

# 控件
sx = w.FloatSlider(value=0.0, min=-1.0, max=1.0, step=0.01, description='x')
sy = w.FloatSlider(value=0.0, min=-1.0, max=1.0, step=0.01, description='y')
sz = w.FloatSlider(value=0.0, min=-1.0, max=1.0, step=0.01, description='z')
sroll  = w.FloatSlider(value=0.0, min=-180.0, max=180.0, step=1.0, description='roll°')
spitch = w.FloatSlider(value=0.0, min=-180.0, max=180.0, step=1.0, description='pitch°')
syaw   = w.FloatSlider(value=0.0, min=-180.0, max=180.0, step=1.0, description='yaw°')
L = w.FloatSlider(value=0.2, min=0.05, max=0.5, step=0.01, description='axis_len')
show_world = w.Checkbox(value=True, description='显示世界坐标轴')
reset_btn = w.Button(description='重置')

# 初始世界坐标轴
world = None
if show_world.value:
    world = plot_transform(ax, A2B=np.eye(4), s=0.25)

h_frame = None  # 当前坐标轴句柄（pytransform3d 返回艺术家对象列表）

def draw_pose(*_):
    global h_frame, world
    # 清掉旧的坐标轴艺术家（不清整张图，避免闪烁）
    if h_frame:
        for artist in h_frame:
            try:
                artist.remove()
            except Exception:
                pass
        h_frame = None
    if world and not show_world.value:
        for a in world:
            try: a.remove()
            except Exception: pass
        world = None
    elif (not world) and show_world.value:
        world = plot_transform(ax, A2B=np.eye(4), s=0.25)

    # 角度转弧度
    r = np.deg2rad(sroll.value)
    p = np.deg2rad(spitch.value)
    y = np.deg2rad(syaw.value)

    R = matrix_from_euler([r, p, y],0,1,2,True)  # roll->pitch->yaw
    t = np.array([sx.value, sy.value, sz.value])
    T = transform_from(R, t)

    # 画变换后的坐标轴
    artists = plot_transform(ax, A2B=T, s=L.value)
    # 保存以便删除
    globals()['h_frame'] = artists

    # 维持合适视野
    ax.figure.canvas.draw_idle()

def on_reset(_):
    sx.value = 0.0; sy.value = 0.0; sz.value = 0.0
    sroll.value = spitch.value = syaw.value = 0.0
    L.value = 0.2
    show_world.value = True

for wid in (sx, sy, sz, sroll, spitch, syaw, L, show_world):
    wid.observe(draw_pose, names='value')
reset_btn.on_click(on_reset)

controls = w.VBox([
    w.HBox([sx, sy, sz]),
    w.HBox([sroll, spitch, syaw]),
    w.HBox([L, show_world, reset_btn]),
])
# display(controls)

# 首次绘制
draw_pose()
