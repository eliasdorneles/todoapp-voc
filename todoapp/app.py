import android
from android.graphics import Paint
from android.view import ViewGroup
from android.widget import CheckBox, LinearLayout, ListView, TextView


class OnClick(implements=android.view.View[OnClickListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onClick(self, view: android.view.View) -> void:
        self.callback(*self.args, **self.kwargs)


class StrikeableTextView(extends=android.widget.TextView):
    @super({context: android.content.Context})
    def __init__(self, context, striked=False):
        self.striked = striked
        self._repaint_strike()

    def setStriked(self, striked):
        self.striked = bool(striked)
        self._repaint_strike()

    def _repaint_strike(self):
        if self.striked:
            flags = self.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG
            self.setTextColor(0xffaaaaaa)
        else:
            flags = self.getPaintFlags() & ~Paint.STRIKE_THRU_TEXT_FLAG
            self.setTextColor(0xff111111)
        self.setPaintFlags(flags)


class TodoItem:
    def __init__(self, text, context, striked=False, layout=None):
        self.context = context
        if layout:
            self.layout = layout
            self.checkbox = layout.getChildAt(0)
            self.text_view = layout.getChildAt(1)
        else:
            self.layout = LinearLayout(self.context)
            self.checkbox = CheckBox(self.context)
            self.checkbox.setOnClickListener(OnClick(self.update))
            self.layout.addView(self.checkbox)
            self.text_view = StrikeableTextView(self.context, striked=False)
            self.text_view.setTextSize(25)
            self.layout.addView(self.text_view)
        self.text_view.setText(text)

    def update(self):
        self.text_view.setStriked(self.checkbox.isChecked())

    def getView(self):
        return self.layout


class ListAdapter(extends=android.widget.BaseAdapter):
    def __init__(self, context, values):
        self.context = context
        self.values = list(values)

    def getCount(self) -> int:
        return len(self.values)

    def getItem(self, position: int) -> java.lang.Object:
        return self.values[position]

    def getItemId(self, position: int) -> long:
        return hash(self.values[position])

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        text = self.getItem(position)
        if view is None:
            todo = TodoItem(text, self.context, striked=position % 2 == 0)
        else:
            todo = TodoItem(text, self.context, layout=view)
        return todo.getView()


class MainApp:
    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)

    def onCreate(self):
        print('Starting TodoApp')
        # TODO: sync this with a sqlite database
        items = [
            "get ice cream",
            "call mom",
            "buy plane tickets",
            "reserve hotel",
        ]
        adapter = ListAdapter(self._activity, items)
        listView = ListView(self._activity)
        listView.setAdapter(adapter)

        vlayout = LinearLayout(self._activity)
        vlayout.setOrientation(LinearLayout.VERTICAL)
        vlayout.addView(listView)

        self._activity.setContentView(vlayout)


def main():
    MainApp()
