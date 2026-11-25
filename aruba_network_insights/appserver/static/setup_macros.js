/*
 * Aruba Network Insights - Configuration page logic.
 * Loads the current definitions of the index macros and writes them back via
 * the splunkd REST proxy on Save. No restart needed (search macros are search-time).
 */
require(['jquery', 'splunkjs/mvc', 'splunkjs/mvc/simplexml/ready!'], function ($, mvc) {
    'use strict';

    var APP = 'aruba_network_insights';
    var MACROS = [
        { name: 'aruba_central_index', field: '#aruba_central_index_def', example: 'index=aruba' },
        { name: 'aruba_syslog_index', field: '#aruba_syslog_index_def', example: 'index=netops' }
    ];

    var service = mvc.createService({ owner: 'nobody', app: APP });

    function macroUrl(name) {
        return 'configs/conf-macros/' + encodeURIComponent(name);
    }

    function setStatus(msg, kind) {
        var el = $('#aruba_setup_status');
        el.text(msg);
        el.removeClass('ok err busy').addClass(kind || '');
    }

    // Load the current definitions into the inputs.
    $.each(MACROS, function (i, m) {
        service.get(macroUrl(m.name), { output_mode: 'json' }, function (err, resp) {
            if (err) { return; }
            try {
                $(m.field).val(resp.data.entry[0].content.definition || '');
            } catch (e) { /* macro may not exist yet */ }
        });
    });

    function saveMacro(m, def) {
        return $.Deferred(function (d) {
            service.post(macroUrl(m.name), { definition: def }, function (err) {
                if (err) { d.reject(m.name); } else { d.resolve(); }
            });
        }).promise();
    }

    function markConfigured() {
        // Flip is_configured so the app no longer shows the setup hint.
        return $.Deferred(function (d) {
            service.post('apps/local/' + APP, { configured: 1 }, function () { d.resolve(); });
        }).promise();
    }

    function refreshChecks() {
        $.each(['aruba_source_check'], function (i, id) {
            var manager = mvc.Components.get(id);
            if (manager) { manager.startSearch(); }
        });
    }

    $(document).on('click', '#aruba_setup_save', function () {
        var defs = [];
        for (var i = 0; i < MACROS.length; i++) {
            var m = MACROS[i];
            var def = $.trim($(m.field).val());
            if (!def) {
                setStatus('Enter a search expression for ' + m.name + ', for example ' + m.example + '.', 'err');
                return;
            }
            if (/[|`\r\n]/.test(def)) {
                setStatus('The definition of ' + m.name + ' must be a plain search expression. Pipes, backticks and line breaks are not allowed.', 'err');
                return;
            }
            defs.push(def);
        }
        setStatus('Saving\u2026', 'busy');
        $.when.apply($, $.map(MACROS, function (m, i) { return saveMacro(m, defs[i]); }))
            .done(function () {
                markConfigured().always(function () {
                    setStatus('Saved. All dashboards use the new indexes now.', 'ok');
                    refreshChecks();
                });
            })
            .fail(function (name) {
                setStatus('Saving ' + name + ' failed. You need write access to the app. You can also edit the macro under Settings \u2192 Advanced search \u2192 Search macros.', 'err');
            });
    });
});
