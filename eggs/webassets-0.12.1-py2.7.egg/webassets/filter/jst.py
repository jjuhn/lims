import os
import re
try:
    import json
except ImportError:
    import simplejson as json
from webassets.filter import Filter
from webassets.utils import common_path_prefix


__all__ = ('JST',)


class JSTemplateFilter(Filter):
    """Common base class for the JST and Handlebars filters, and
    possibly other Javascript templating systems in the future.
    """

    def concat(self, out, hunks, **kwargs):
        self.process_templates(out, hunks, **kwargs)

    def process_templates(self, out, hunks, **kw):
        raise NotImplementedError()

    def iter_templates_with_base(self, hunks):
        """Helper that for list of ``hunks``, as given to
        ``concat()``, yields 2-tuples of (name, hunk), with name
        being the name of the source file relative to the common
        prefix of all source files.

        In other words, each template gets the shortest possible
        name to identify it.
        """
        base_path = self._find_base_path(
            [info['source_path'] for _, info in hunks]) + os.path.sep
        for hunk, info in hunks:
            name = info['source_path']
            name = name[len(base_path):]
            name = os.path.splitext(name)[0]
            yield name, hunk

    def _find_base_path(self, paths):
        """Hmmm.  There should aways be some common base path."""
        if len(paths) == 1:
            return os.path.dirname(paths[0])
        return common_path_prefix(paths)


class JST(JSTemplateFilter):
    """This filter processes generic JavaScript templates. It will generate
    JavaScript code that runs all files through a template compiler, and makes
    the templates available as an object.

    It was inspired by `Jammit`_.

    For example, if you have a file named ``license.jst``:

    .. code-block:: html

        <div class="drivers-license">
          <h2>Name: <%= name %></h2>
          <em>Hometown: <%= birthplace %></em>
        </div>

    Then, after applying this filter, you could use the template in JavaScript:

    .. code-block:: javascript

        JST.license({name : "Moe", birthplace : "Brooklyn"});

    The name of each template is derived from the filename. If your JST files
    are spread over different directories, the path up to the common prefix
    will be included. For example::

        Bundle('templates/app1/license.jst', 'templates/app2/profile.jst',
               filters='jst')

    will make the templates available as ``app1/license`` and ``app2/profile``.

    .. note::
        The filter is "generic" in the sense that it does not actually compile
        the templates, but wraps them in a JavaScript function call, and can
        thus be used with any template language. webassets also has filters
        for specific JavaScript template languages like
        :class:`~.filter.dust.DustJS` or
        :class:`~.filter.handlebars.Handlebars`, and those filters precompile
        the templates on the server, which means a performance boost on the
        client-side.

    Unless configured otherwise, the filter will use the same micro-templating
    language that `Jammit`_ uses, which is turn is the same one that is
    available in `underscore.js`_. The JavaScript code necessary to compile
    such templates will implicitly be included in the filter output.

    *Supported configuration options:*

    JST_COMPILER (template_function)
        A string that is inserted into the generated JavaScript code in place
        of the function to be called that should do the compiling. Unless you
        specify a custom function here, the filter will include the JavaScript
        code of it's own micro-templating language, which is the one used by
        `underscore.js`_ and `Jammit`_.

        If you assign a custom function, it is your responsibility to ensure
        that it is available in your final JavaScript.

        If this option is set to ``False``, then the template strings will be
        output directly, which is to say, ``JST.foo`` will be a string holding
        the raw source of the ``foo`` template.

    JST_NAMESPACE (namespace)
        How the templates should be made available in JavaScript. Defaults to
        ``window.JST``, which gives you a global ``JST`` object.

    JST_BARE (bare)
        Whether everything generated by this filter should be wrapped inside
        an anonymous function. Default to ``False``.

        .. note::

            If you enable this option, the namespace must be a property
            of the ``window`` object, or you won't be able to access the
            templates.

    JST_DIR_SEPARATOR (separator)
        The separator character to use for templates within directories.
        Defaults to '/'

    .. _Jammit:
    .. _underscore.js: http://documentcloud.github.com/underscore/#template
    """
    name = 'jst'
    options = {
        # The JavaScript compiler function to use
        'template_function': 'JST_COMPILER',
        # The JavaScript namespace to put templates in
        'namespace': 'JST_NAMESPACE',
        # Wrap everything in a closure
        'bare': 'JST_BARE',
        # The path separator to use with templates in different directories
        'separator': 'JST_DIR_SEPARATOR'
    }
    max_debug_level = None

    def setup(self):
        super(JST, self).setup()
        self.include_jst_script = (self.template_function == 'template') \
                                  or self.template_function is None

    def process_templates(self, out, hunks, **kwargs):
        namespace = self.namespace or 'window.JST'

        if self.bare is False:
            out.write("(function(){\n")

        out.write("%s = %s || {};\n" % (namespace, namespace))

        if self.include_jst_script:
            out.write("%s\n" % _jst_script)

        for name, hunk in self.iter_templates_with_base(hunks):
            # Make it a valid Javascript string.
            contents = json.dumps(hunk.data())

            out.write("%s['%s'] = " % (namespace, self._get_jst_name(name)))
            if self.template_function is False:
                out.write("%s;\n" % (contents))
            else:
                out.write("%s(%s);\n" % (
                    self.template_function or 'template', contents))

        if self.bare is False:
            out.write("})();")

    def _get_jst_name(self, name):
        """Return the name for the JST with any path separators normalised"""
        return _path_separator_re.sub(self.separator or "/", name)


_path_separator_re = re.compile(r'[/\\]+')

_jst_script = 'var template = function(str){var fn = new Function(\'obj\', \'var \
__p=[],print=function(){__p.push.apply(__p,arguments);};\
with(obj||{}){__p.push(\\\'\'+str.replace(/\\\\/g, \'\\\\\\\\\')\
.replace(/\'/g, "\\\\\'").replace(/<%=([\\s\\S]+?)%>/g,\
function(match,code){return "\',"+code.replace(/\\\\\'/g, "\'")+",\'";})\
.replace(/<%([\\s\\S]+?)%>/g,function(match,code){return "\');"+code\
.replace(/\\\\\'/g, "\'").replace(/[\\r\\n\\t]/g,\' \')+"__p.push(\'";})\
.replace(/\\r/g,\'\\\\r\').replace(/\\n/g,\'\\\\n\')\
.replace(/\\t/g,\'\\\\t\')+"\');}return __p.join(\'\');");return fn;};'
