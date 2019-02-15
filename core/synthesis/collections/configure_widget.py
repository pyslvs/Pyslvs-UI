# -*- coding: utf-8 -*-

"""The widget of 'Triangular iteration' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TYPE_CHECKING,
    List,
    Tuple,
    Sequence,
    Set,
    Dict,
    Callable,
    Any,
)
from math import hypot
import pprint
from core.QtModules import (
    Signal,
    QWidget,
    Slot,
    QMessageBox,
    QInputDialog,
    QListWidgetItem,
    QLabel,
    QApplication,
)
from core.graphics import PreviewCanvas
from core.libs import (
    Graph,
    edges_view,
    graph2vpoints,
    parse_pos,
)
from .dialogs import (
    CollectionsDialog,
    CustomsDialog,
    TargetsDialog,
    list_texts,
)
from .Ui_configure_widget import Ui_Form

if TYPE_CHECKING:
    from core.widgets.custom import MainWindowBase


class _ConfigureCanvas(PreviewCanvas):

    """Customized preview window has some functions of mouse interaction.

    Emit signal call to change current point when pressed a dot.
    """

    set_joint_number = Signal(int)

    def __init__(self, parent: QWidget):
        """Add a function use to get current point from parent."""
        super(_ConfigureCanvas, self).__init__(parent)
        self.pressed = False
        self.get_joint_number = parent.joint_name.currentIndex

    def mousePressEvent(self, event):
        """Check if get close to a joint."""
        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom

        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue

            if hypot(x - mx, y - my) <= 5:
                self.set_joint_number.emit(node)
                self.pressed = True
                break

    def mouseReleaseEvent(self, event):
        """Cancel the drag."""
        self.pressed = False

    def mouseMoveEvent(self, event):
        """Drag to move the joint."""
        if not self.pressed:
            return

        row = self.get_joint_number()
        if not row > -1:
            return

        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom
        if -120 <= mx <= 120:
            self.pos[row] = (mx, self.pos[row][1])
        else:
            self.pos[row] = (120 if -120 <= mx else -120, self.pos[row][1])
        if -120 <= my <= 120:
            self.pos[row] = (self.pos[row][0], my)
        else:
            self.pos[row] = (self.pos[row][0], 120 if -120 <= my else -120)
        self.update()


def _set_warning(label: QLabel, warning: bool):
    """Show a warning sign front of label."""
    warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "
    label.setText(label.text().replace(warning_icon, ''))
    if warning:
        label.setText(warning_icon + label.text())


class ConfigureWidget(QWidget, Ui_Form):

    """Configure widget.

    This interface use to modify structure profile.
    """

    def __init__(
        self,
        add_collection: Callable[[Sequence[Tuple[int, int]]], None],
        parent: 'MainWindowBase'
    ):
        """We need some function from structure collections."""
        super(ConfigureWidget, self).__init__(parent)
        self.setupUi(self)
        self.unsave_func = parent.workbook_no_save
        self.get_configure = parent.get_configure
        self.add_collection = add_collection

        # Iteration data.
        self.collections: Dict[str, Dict[str, Any]] = {}

        # Customized preview canvas.
        self.configure_canvas = _ConfigureCanvas(self)
        self.configure_canvas.set_joint_number.connect(
            self.joint_name.setCurrentIndex
        )
        self.main_layout.insertWidget(0, self.configure_canvas)
        self.main_splitter.setSizes([300, 300])

        self.__clear_panel()

    def add_collections(self, collections: Dict[str, Dict[str, Any]]):
        """Update the new collections."""
        self.collections.update(collections)

    def clear(self):
        """Clear all sub-widgets."""
        self.collections.clear()
        self.__clear_panel()

    def __clear_panel(self):
        """Clear the settings of sub-widgets."""
        self.profile_name = ""
        self.configure_canvas.clear()
        self.joint_name.clear()
        self.grounded_list.clear()
        self.driver_list.clear()
        self.follower_list.clear()
        self.target_list.clear()
        self.expr_show.clear()
        for label in [
            self.grounded_label,
            self.driver_label,
            self.follower_label,
            self.target_label,
        ]:
            _set_warning(label, True)

    @Slot(name='on_clear_button_clicked')
    def __user_clear(self):
        """Ask user before clear."""
        if QMessageBox.question(
            self,
            "New profile",
            "Triangular iteration should be added structure diagrams "
            "from structure collections.\n"
            "Do you want to create a new profile?"
        ) == QMessageBox.Yes:
            self.__clear_panel()

    @Slot(name='on_add_collection_button_clicked')
    def __add_collection(self):
        """Add the graph back to structure collections."""
        self.add_collection(tuple(self.configure_canvas.G.edges))

    @Slot(Graph, dict)
    def set_graph(
        self,
        graph: Graph,
        pos: Dict[int, Tuple[float, float]]
    ):
        """Set the graph to preview canvas."""
        self.__clear_panel()
        self.configure_canvas.set_graph(graph, pos)
        ev = dict(edges_view(graph))
        joints_count = set()

        for l1, l2 in ev.values():
            joints_count.update({l1, l2})

        links = [[] for _ in range(len(joints_count))]

        for joint, link in ev.items():
            for node in link:
                links[node].append(joint)

        for link in links:
            points_text = ", ".join(f'P{node}' for node in link)
            self.grounded_list.addItem(f"({points_text})")

        # Point name as (P1, P2, P3, ...).
        for node in pos:
            self.joint_name.addItem(f'P{node}')

    @Slot(int, name='on_grounded_list_currentRowChanged')
    def __set_ground(self, row: int):
        """Change current grounded link. Reset all settings."""
        has_choose = row > -1
        _set_warning(self.grounded_label, not has_choose)
        self.configure_canvas.set_grounded(row)
        self.follower_list.clear()
        self.driver_list.clear()
        self.driver_base.clear()
        self.driver_rotator.clear()
        if has_choose:
            items = (
                self.grounded_list.item(row).text()
                .replace('(', '')
                .replace(')', '')
                .split(", ")
            )
            self.follower_list.addItems(items)
            self.driver_base.addItems(items)

        _set_warning(self.follower_label, not has_choose)
        _set_warning(self.driver_label, True)
        if row == self.grounded_list.currentRow():
            return

        self.grounded_list.blockSignals(True)
        self.grounded_list.setCurrentRow(row)
        self.grounded_list.blockSignals(False)

    @Slot(str, name='on_driver_base_currentIndexChanged')
    def __set_driver_base(self, name: str):
        self.driver_rotator.clear()
        if not name:
            return

        def find_friends(node: int):
            """Find all the nodes that are same link with input node."""
            ev = dict(edges_view(self.configure_canvas.G))
            link = set(ev[node])
            tmp_list = []
            for node_, link_ in ev.items():
                if node_ == node:
                    continue
                if set(link_) & link:
                    tmp_list.append(f'P{node_}')
            return tmp_list

        self.driver_rotator.addItems(find_friends(int(name.replace('P', ''))))

    @Slot(name='on_driver_add_clicked')
    def __add_driver(self):
        """Add a input pair."""
        d1 = self.driver_base.currentText()
        d2 = self.driver_rotator.currentText()
        if d1 == d2 == "":
            return

        d1_d2 = f"({d1}, {d2})"
        for n in list_texts(self.driver_list):
            if n == d1_d2:
                return

        self.driver_list.addItem(d1_d2)
        self.configure_canvas.set_driver([
            eval(n.replace('P', ''))[0] for n in list_texts(self.driver_list)
        ])
        _set_warning(self.driver_label, False)

    @Slot(name='on_driver_del_clicked')
    def __add_follower(self):
        """Remove a input pair."""
        row = self.driver_list.currentRow()
        if not row > -1:
            return

        self.driver_list.takeItem(row)
        _set_warning(self.driver_label, self.driver_list.count() == 0)

    @Slot(name='on_add_customization_clicked')
    def __add_cus(self):
        """Show up custom joints dialog."""
        dlg = CustomsDialog(self)
        dlg.show()
        dlg.exec()
        self.configure_canvas.update()

    def __get_current_mechanism_params(self) -> Dict[str, Any]:
        """Get the current mechanism parameters."""
        self.__set_parm_bind()

        input_list = []
        for s in list_texts(self.driver_list):
            pair: Tuple[int, int] = eval(s.replace('P', ''))
            if set(pair) & set(self.configure_canvas.same):
                continue
            input_list.append(pair)

        place_list = {}
        for s in list_texts(self.follower_list):
            joint = int(s.replace('P', ''))
            if joint in self.configure_canvas.same:
                continue
            place_list[joint] = None

        target_list = {}
        for s in list_texts(self.target_list):
            target_list[int(s.replace('P', ''))] = None

        return {
            'Expression': self.expr_show.text(),
            'input': input_list,
            'Graph': self.configure_canvas.G.edges,
            'Placement': place_list,
            'Target': target_list,
            'cus': self.configure_canvas.cus.copy(),
            'same': self.configure_canvas.same.copy(),
        }

    @Slot(name='on_load_button_clicked')
    def __load_data_base(self):
        """Show up the dialog to load structure data."""
        dlg = CollectionsDialog(
            self.collections,
            self.get_configure,
            self
        )
        dlg.show()
        if not dlg.exec():
            return

        self.profile_name = dlg.name()
        params = dlg.params()

        # Add customize joints.
        graph = Graph(params['Graph'])
        expression: str = params['Expression']
        pos_list = parse_pos(expression)
        cus: Dict[int, int] = params['cus']
        same: Dict[int, int] = params['same']
        for node, ref in sorted(same.items()):
            pos_list.insert(node, pos_list[ref])
        pos: Dict[int, Tuple[float, float]] = dict(enumerate(pos_list))
        self.set_graph(graph, pos)
        self.configure_canvas.cus = cus
        self.configure_canvas.same = same

        # Grounded setting.
        placement: Set[int] = set(params['Placement'])
        for row, link in enumerate(graph.nodes):
            if placement <= {n for n, edge in edges_view(graph) if link in edge}:
                self.__set_ground(row)
                break

        # Driver, Follower, Target
        inputs: List[Tuple[int, int]] = params['input']
        self.driver_list.addItems(f"(P{b}, P{d})" for b, d in inputs)
        _set_warning(self.driver_label, self.driver_list.count() == 0)
        target_list: List[int] = params['Target']
        self.target_list.addItems(f"P{n}" for n in target_list)
        _set_warning(self.target_label, self.target_list.count() == 0)

        # Expression
        self.expr_show.setText(params['Expression'])

    @Slot(name='on_target_button_clicked')
    def __set_target(self):
        """Show up target joints dialog."""
        dlg = TargetsDialog(self)
        dlg.show()
        if not dlg.exec():
            return
        self.target_list.clear()
        for target in list_texts(dlg.targets_list):
            self.target_list.addItem(target)
        _set_warning(self.target_label, self.target_list.count() == 0)

    @Slot(QListWidgetItem)
    def __set_parm_bind(self, _: QListWidgetItem = None):
        """Set parameters binding."""
        link_expr_list = []
        for row, gs in enumerate(list_texts(self.grounded_list)):
            try:
                link_expr = []
                # Links from grounded list.
                for name in gs.replace('(', '').replace(')', '').split(", "):
                    num = int(name.replace('P', ''))
                    if num in self.configure_canvas.same:
                        name = f'P{self.configure_canvas.same[num]}'
                    link_expr.append(name)
            except KeyError:
                continue
            else:
                # Customize joints.
                for joint, link in self.configure_canvas.cus.items():
                    if row == link:
                        link_expr.append(f"P{joint}")
                link_expr_str = ','.join(sorted(set(link_expr)))
                if row == self.grounded_list.currentRow():
                    link_expr_list.insert(0, link_expr_str)
                else:
                    link_expr_list.append(link_expr_str)

        self.expr_show.setText("M[" + ", ".join(vp.expr() for vp in graph2vpoints(
            self.configure_canvas.G,
            self.configure_canvas.pos,
            self.configure_canvas.cus,
            self.configure_canvas.same,
            self.grounded_list.currentRow()
        )) + "]")

    @Slot(name='on_save_button_clicked')
    def __save(self):
        """Save the profile to database."""
        if self.profile_name:
            name = self.profile_name
            ok = True
        else:
            name, ok = QInputDialog.getText(
                self,
                "Profile name",
                "Please enter the profile name:"
            )
        if not ok:
            return
        i = 0
        while (name not in self.collections) and (not name):
            name = f"Structure_{i}"
        self.collections[name] = self.__get_current_mechanism_params()
        self.profile_name = name
        self.unsave_func()

    @Slot(name='on_clipboard_button_clicked')
    def __copy(self):
        """Copy the mechanism params."""
        QApplication.clipboard().setText(
            pprint.pformat(self.__get_current_mechanism_params())
        )