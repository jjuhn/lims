var extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

import {
  ButtonTool,
  ButtonToolView,
  ButtonToolButtonView
} from "../button_tool";

export var ActionToolButtonView = (function(superClass) {
  extend(ActionToolButtonView, superClass);

  function ActionToolButtonView() {
    return ActionToolButtonView.__super__.constructor.apply(this, arguments);
  }

  ActionToolButtonView.prototype._clicked = function() {
    return this.model.trigger('do');
  };

  return ActionToolButtonView;

})(ButtonToolButtonView);

export var ActionToolView = (function(superClass) {
  extend(ActionToolView, superClass);

  function ActionToolView() {
    return ActionToolView.__super__.constructor.apply(this, arguments);
  }

  ActionToolView.prototype.initialize = function(options) {
    ActionToolView.__super__.initialize.call(this, options);
    return this.listenTo(this.model, 'do', this["do"]);
  };

  return ActionToolView;

})(ButtonToolView);

export var ActionTool = (function(superClass) {
  extend(ActionTool, superClass);

  function ActionTool() {
    return ActionTool.__super__.constructor.apply(this, arguments);
  }

  return ActionTool;

})(ButtonTool);
