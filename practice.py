import urwid
from difflib import SequenceMatcher

from snippet import Snippet

g_verse = None    # placeholder for currently selected verse
g_verse = Snippet.random()

def do_diff(text, n_text):
    seqm = SequenceMatcher(None, text, n_text)
    output_orig = []
    output_new = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        orig_seq = seqm.a[a0:a1]
        new_seq = seqm.b[b0:b1]
        if opcode == 'equal':
            output_orig.append(orig_seq)
            output_new.append(orig_seq)
        elif opcode == 'insert':
            output_new.append(('extra_text', new_seq))
        elif opcode == 'delete':
            output_orig.append(('missing_text', orig_seq))
        elif opcode == 'replace':
            output_new.append(('wrong_text', new_seq))
            output_orig.append(('wrong_text', orig_seq))
        else:
            raise('Error')
    return output_orig, output_new, seqm.quick_ratio()


palette = [('I say', 'default,bold', 'default', 'bold'),
           ('missing_text', 'bold,light red', 'default', 'default'),
           ('extra_text', 'bold,light green', 'default', 'default'),
           ('wrong_text', 'bold,light cyan', 'default', 'default'),
           ]

verse = urwid.Text(g_verse.contents)
reference = urwid.Text(g_verse.reference)
user_input = urwid.Edit(('I say', u"\nType to Practice:\n"))
score = urwid.Text(u"")
exit_btn = urwid.Button(u'Exit')
next_btn = urwid.Button(u'Next')
div = urwid.Divider()
pile = urwid.Pile([verse, reference, user_input, div, score, div, next_btn, exit_btn])
top = urwid.Filler(pile, valign='top')

def recite(button):
    # TODO: randomly select unique Snippet
    # TODO: show reference
    # TODO: if practice, show contents
    global g_verse
    g_verse = Snippet.random()

    verse.set_text(g_verse.contents)
    reference.set_text(g_verse.reference)

    user_input.set_edit_text(u"")

def answer(edit, new_edit_text):
    # TODO: style incorrect words
    orig_text, new_text, ratio = do_diff(g_verse.contents.lower(),
                                         new_edit_text.lower())

    if ratio == 1.0:
        score.set_text(u"Perfect!")
    else:
        text = []
        text.append(u"Match: %f" % ratio)
        text.append("\n")
        text.extend(orig_text)
        text.append("\n")
        text.extend(new_text)

        score.set_text(text)

def on_exit_clicked(button):
    raise urwid.ExitMainLoop()


urwid.connect_signal(next_btn, 'click', recite)
urwid.connect_signal(exit_btn, 'click', on_exit_clicked)
urwid.connect_signal(user_input, 'change', answer)

urwid.MainLoop(top, palette).run()
