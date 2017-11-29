import android
from android.graphics import Paint
from android.view import ViewGroup
from android.content import ContentValues
from android.widget import CheckBox, LinearLayout, ListView, TextView
from android.database.sqlite import SQLiteDatabase


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
    def __init__(self, value, context, layout=None, callback=None):
        self.callback = callback
        self.context = context
        self.value = value
        if layout:
            self.layout = layout
            self.checkbox = layout.getChildAt(0)
            self.text_view = layout.getChildAt(1)
        else:
            self.layout = LinearLayout(self.context)
            self.checkbox = CheckBox(self.context)
            self.checkbox.setOnClickListener(OnClick(self.update))
            self.layout.addView(self.checkbox)
            self.text_view = StrikeableTextView(self.context, striked=value['finished'])
            self.text_view.setTextSize(25)
            self.layout.addView(self.text_view)
        self.text_view.setText(value['title'])
        self.checkbox.setChecked(value['finished'])

    def update(self):
        self.value['finished'] = self.checkbox.isChecked()
        self.text_view.setStriked(self.value['finished'])
        self.callback(self.value)

    def getView(self):
        return self.layout


class ListAdapter(extends=android.widget.BaseAdapter):
    def __init__(self, context, values, listener=None):
        self.listener = listener
        self.context = context
        self.values = list(values)

    def getCount(self) -> int:
        return len(self.values)

    def getItem(self, position: int) -> java.lang.Object:
        return self.values[position]

    def getItemId(self, position: int) -> long:
        return self.values[position]['id']

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        value = self.getItem(position)
        if view is None:
            todo = TodoItem(value, self.context, callback=self.listener)
        else:
            todo = TodoItem(value, self.context, layout=view, callback=self.listener)
        return todo.getView()


class TodoDB(extends=android.database.sqlite.SQLiteOpenHelper):
    @super({
        context: android.content.Context,
        "org.pybee.elias.todoapp": java.lang.String,
        None: android.database.sqlite.SQLiteDatabase[CursorFactory],
        1: int
    })
    def __init__(self, context):
        pass

    def onCreate(self, db: android.database.sqlite.SQLiteDatabase) -> void:
        print('initiating TodoDB')
        db.execSQL(
            "CREATE TABLE todo ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "title TEXT NOT NULL,"
            "finished BOOLEAN NOT NULL CHECK (finished IN (0,1))"
            ")"
        )

    def onUpgrade(self, db: android.database.sqlite.SQLiteDatabase,
                  oldVersion: int, newVersion: int) -> void:
        print('will upgrade database from', oldVersion, ' to', newVersion)
        raise NotImplementedError

    def add_item(self, item, finished=False):
        values = ContentValues()
        values.put("title", item)
        values.put("finished", finished)
        db = self.getWritableDatabase()
        db.insertWithOnConflict("todo", None, values, SQLiteDatabase.CONFLICT_REPLACE)
        db.close()

    def fetch_items(self):
        result = []

        db = self.getReadableDatabase()
        cursor = db.rawQuery("SELECT * FROM todo", None)
        while cursor.moveToNext():
            item_id = int(cursor.getInt(cursor.getColumnIndex('id')))
            title = cursor.getString(cursor.getColumnIndex('title'))
            finished = cursor.getInt(cursor.getColumnIndex('finished'))
            result.append(dict(id=item_id, title=title, finished=bool(finished)))
        db.close()

        return result

    def update_item(self, value):
        db = self.getWritableDatabase()
        db.execSQL(
            "UPDATE todo SET finished=%d WHERE id=%d"%(int(value['finished']), value['id'])
        )
        db.close()

class MainApp:
    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)
        self.db = TodoDB(self._activity)

    def _populate_db(self):
        self.db.add_item("get ice cream", finished=True)
        self.db.add_item("call mom", finished=False)
        self.db.add_item("buy plane tickets", finished=False)
        self.db.add_item("reserve hotel", finished=False)

    def onCreate(self):
        print('Starting TodoApp')
        dbitems = self.db.fetch_items()

        if not dbitems:
            print('populating DB')
            self._populate_db()
            dbitems = self.db.fetch_items()

        print('dbitems', dbitems)

        adapter = ListAdapter(self._activity, dbitems, listener=self.update_item)
        listView = ListView(self._activity)
        listView.setAdapter(adapter)

        vlayout = LinearLayout(self._activity)
        vlayout.setOrientation(LinearLayout.VERTICAL)
        vlayout.addView(listView)

        self._activity.setContentView(vlayout)

    def update_item(self, value):
        self.db.update_item(value)

def main():
    MainApp()
