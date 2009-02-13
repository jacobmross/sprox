"""
fillerbase Module

Classes to help fill widgets with data

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""

from sprox.formbase import FormBase, EditableForm, AddRecordForm
from sprox.widgetselector import SAWidgetSelector
from sprox.widgets.dojo import SproxDojoSelectShuttleField

class DojoSAWidgetSelector(SAWidgetSelector):
    """Dojo-Specific Widget Selector"""
    default_multiple_select_field_widget_type = SproxDojoSelectShuttleField

class DojoFormBase(FormBase):
    """FormBase for Dojo

    see :class:`sprox.formbase.FormBase`
    
    """
    __widget_selector_type__ = DojoSAWidgetSelector
    
class DojoEditableForm(EditableForm):
    """Creates a form for editing records that has select shuttles for the multiple relations.
    
    :Modifiers:
      see :class:`sprox.formbase.FormBase`

    :Usage:
    
    >>> from sprox.dojo.formbase import DojoAddRecordForm
    >>> from formencode import Schema
    >>> from formencode.validators import FieldsMatch
    >>> class Form(DojoAddRecordForm):
    ...     __model__ = User
    ...     __limit_fields__       = ['user_name', 'groups']
    >>> add_form = Form()
    >>> print add_form()
    <form xmlns="http://www.w3.org/1999/xhtml" action="" method="post" class="has_error required tableform">
        <div>
                <input type="hidden" name="sprox_id" class="has_error hiddenfield" id="sprox_id" />
                <span class="fielderror">Missing value</span>
        </div>
        <table border="0" cellspacing="0" cellpadding="2">
            <tr id="user_name.container" class="even" title="">
                <td class="labelcol">
                    <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
                </td>
                <td class="fieldcol">
                    <input type="text" name="user_name" class="textfield" id="user_name" value="" />
                </td>
            </tr><tr id=".container" class="odd" title="">
                <td class="labelcol">
                    <label id=".label" for="" class="fieldlabel">Groups</label>
                </td>
                <td class="fieldcol">
                    <div dojoType="twdojo.SelectShuttle" id="groups_SelectShuttle">
        <div style="float:left; padding: 5px; width:10em;">
            Available<br />
            <select class="shuttle" id="groups_src" multiple="multiple" name="" size="5">
                    <option value="1">0</option><option value="2">1</option><option value="3">2</option><option value="4">3</option><option value="5">4</option>
            </select>
        </div>
        <div style="float:left; padding: 25px 5px 5px 0px;" id="groups_Buttons">
            <button class="shuttle" id="groups_AllRightButton">&gt;&gt;</button><br />
            <button class="shuttle" id="groups_RightButton">&gt;</button><br />
            <button class="shuttle" id="groups_LeftButton">&lt;</button><br />
            <button class="shuttle" id="groups_AllLeftButton">&lt;&lt;</button>
        </div>
        <div style="float:left; padding: 5px; width:10em;">
                Selected<br />
                <select class="shuttle" id="groups" multiple="multiple" name="groups" size="5">
                </select>
        </div>
        <script type="text/javascript">
        //create an object of this type here
        </script>
    </div>
                </td>
            </tr><tr id="submit.container" class="even" title="">
                <td class="labelcol">
                </td>
                <td class="fieldcol">
                    <input type="submit" class="submitbutton" value="Submit" />
                </td>
            </tr>
        </table>
    </form>
    """

    __widget_selector_type__ = DojoSAWidgetSelector

class DojoAddRecordForm(AddRecordForm):
    """
    Creates a form for adding records that has select shuttles for the multiple relations.
    
    :Modifiers:
      see :class:`sprox.formbase.FormBase`

    :Usage:
    
    >>> from sprox.dojo.formbase import DojoAddRecordForm
    >>> from formencode import Schema
    >>> from formencode.validators import FieldsMatch
    >>> class Form(DojoAddRecordForm):
    ...     __model__ = User
    ...     __limit_fields__       = ['user_name', 'groups']
    >>> add_form = Form()
    >>> print add_form()
    <form xmlns="http://www.w3.org/1999/xhtml" action="" method="post" class="has_error required tableform">
        <div>
                <input type="hidden" name="sprox_id" class="has_error hiddenfield" id="sprox_id" />
                <span class="fielderror">Missing value</span>
        </div>
        <table border="0" cellspacing="0" cellpadding="2">
            <tr id="user_name.container" class="even" title="">
                <td class="labelcol">
                    <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
                </td>
                <td class="fieldcol">
                    <input type="text" name="user_name" class="textfield" id="user_name" value="" />
                </td>
            </tr><tr id=".container" class="odd" title="">
                <td class="labelcol">
                    <label id=".label" for="" class="fieldlabel">Groups</label>
                </td>
                <td class="fieldcol">
                    <div dojoType="twdojo.SelectShuttle" id="groups_SelectShuttle">
        <div style="float:left; padding: 5px; width:10em;">
            Available<br />
            <select class="shuttle" id="groups_src" multiple="multiple" name="" size="5">
                    <option value="1">0</option><option value="2">1</option><option value="3">2</option><option value="4">3</option><option value="5">4</option>
            </select>
        </div>
        <div style="float:left; padding: 25px 5px 5px 0px;" id="groups_Buttons">
            <button class="shuttle" id="groups_AllRightButton">&gt;&gt;</button><br />
            <button class="shuttle" id="groups_RightButton">&gt;</button><br />
            <button class="shuttle" id="groups_LeftButton">&lt;</button><br />
            <button class="shuttle" id="groups_AllLeftButton">&lt;&lt;</button>
        </div>
        <div style="float:left; padding: 5px; width:10em;">
                Selected<br />
                <select class="shuttle" id="groups" multiple="multiple" name="groups" size="5">
                </select>
        </div>
        <script type="text/javascript">
        //create an object of this type here
        </script>
    </div>
                </td>
            </tr><tr id="submit.container" class="even" title="">
                <td class="labelcol">
                </td>
                <td class="fieldcol">
                    <input type="submit" class="submitbutton" value="Submit" />
                </td>
            </tr>
        </table>
    </form>
"""
    __widget_selector_type__ = DojoSAWidgetSelector