import gui
import gui.input as gui_input
import gui.output as gui_output
from db import conn
from helper.session import session


def _apply_session_state():
    if session.count == 0:
        gui_input.question_enable()
        gui_input.toss_enable()
        gui_input.reset_disable()
    elif session.is_complete:
        gui_input.question_disable()
        gui_input.toss_disable()
        gui_input.reset_enable()
    else:
        gui_input.question_disable()
        gui_input.toss_enable()
        gui_input.reset_enable()


def _draw_result():
    true_hex = conn.get_by_binary(session.binary_top_down)
    gui_output.draw_true_info(true_hex)

    if not session.has_stressed_lines:
        gui_output.draw_no_change(true_hex, session.lines)
        return

    reverse_binary = session.reverse_binary_top_down
    gui_output.draw_reverse_hex(reverse_binary)
    gui_output.draw_reverse_info(conn.get_by_binary(reverse_binary))


def _redraw_session():
    for i, line in enumerate(session.lines):
        gui_output.draw_true_line(i, line)

    if session.is_complete:
        _draw_result()


def _on_toss():
    gui_input.reset_enable()
    gui_input.question_disable()

    if session.is_complete:
        return

    line_index = session.count
    line = session.toss_line()
    gui_output.draw_true_line(line_index, line)

    if not session.is_complete:
        return

    gui_input.toss_disable()
    _draw_result()


def _on_reset():
    gui_input.question_enable()
    gui_input.toss_enable()
    gui_input.reset_disable()
    gui_input.question_reset()
    session.reset()
    gui_output.canvas_reset()


def _rebuild_ui():
    """Rebuild all widgets and replay the in-progress session onto them, on a
    resolution or theme change. Hidden while it runs to avoid flicker."""
    gui.root.withdraw()

    question_text = gui_input.get_question()

    gui_input.destroy()
    gui_output.destroy()
    gui.reset_min_height()

    gui.refresh_theme()
    gui_input.build(_on_toss, _on_reset)
    gui_output.build()

    gui_input.set_question(question_text)
    _apply_session_state()
    _redraw_session()

    gui.finalize()


def _preview_theme():
    gui.refresh_theme()
    gui_input.restyle()
    gui_output.restyle()


def main():
    gui.build()
    gui.set_hook('rebuild', _rebuild_ui)
    gui.set_hook('theme_preview', _preview_theme)
    gui.set_hook('background', gui_output.redraw_background)
    gui.set_hook('linestyle', gui_output.redraw_lines)
    gui_input.build(_on_toss, _on_reset)
    gui_output.build()

    gui.finalize()
    gui.root.mainloop()
