import gui
import gui.input as gui_input
import gui.output as gui_output
from db import conn
from helper.session import session


def main():
    def _apply_session_state():
        if session.count == 0:
            gui_input.qstn_enable()
            gui_input.toss_enable()
            gui_input.reset_disable()
        elif session.is_complete:
            gui_input.qstn_disable()
            gui_input.toss_disable()
            gui_input.reset_enable()
        else:
            gui_input.qstn_disable()
            gui_input.toss_enable()
            gui_input.reset_enable()

    def _redraw_session():
        for i, line in enumerate(session.lines):
            gui_output.draw_line_left(i, line)

        if not session.is_complete:
            return

        true_binary = list(reversed(session.binary))
        true_hex = conn.get_by_binary(true_binary)
        gui_output.draw_true_info(true_hex)

        if not session.has_stressed_lines:
            gui_output.draw_no_change(true_hex, session.lines)
            return

        reverse_binary = list(reversed(session.reverse_binary))
        reverse_hex = conn.get_by_binary(reverse_binary)
        gui_output.draw_reverse_hex(reverse_binary)
        gui_output.draw_reverse_info(reverse_hex)

    def _on_toss():
        gui_input.reset_enable()
        gui_input.qstn_disable()

        if session.is_complete:
            return

        line_index = session.count
        line = session.toss_line()
        gui_output.draw_line_left(line_index, line)

        if not session.is_complete:
            return

        gui_input.toss_disable()

        true_binary = list(reversed(session.binary))
        true_hex = conn.get_by_binary(true_binary)
        gui_output.draw_true_info(true_hex)

        if not session.has_stressed_lines:
            gui_output.draw_no_change(true_hex, session.lines)
            return

        reverse_binary = list(reversed(session.reverse_binary))
        reverse_hex = conn.get_by_binary(reverse_binary)
        gui_output.draw_reverse_hex(reverse_binary)
        gui_output.draw_reverse_info(reverse_hex)

    def _on_reset():
        gui_input.qstn_enable()
        gui_input.toss_enable()
        gui_input.reset_disable()
        gui_input.qstn_reset()
        session.reset()
        gui_output.canvas_reset()

    def _rebuild_ui():
        """Destroy and recreate all widgets, then replay the in-progress session
        onto them. Triggered by either a resolution or a theme change (see
        gui.set_rebuild_hook) - hidden while it runs so nothing partially
        restyled/resized flashes on screen mid-rebuild.
        """
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

    gui.build()
    gui.set_rebuild_hook(_rebuild_ui)
    gui_input.build(_on_toss, _on_reset)
    gui_output.build()

    gui.finalize()
    gui.root.mainloop()
