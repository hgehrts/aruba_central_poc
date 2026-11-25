/*
 * Aruba Central POC Dashboards - Configuration page logic.
 * Loads the current definition of the index macro and writes it back via the
 * splunkd REST proxy on Save. No restart needed (search macros are search-time).
 */
require(['jquery', 'splunkjs/mvc', 'splunkjs/mvc/simplexml/ready!'], function ($, mvc) {
    'use strict';

    var APP = 'aruba_central_poc';
    var MACRO = 'aruba_central_index';
    var FIELD = '#aruba_central_index_def';

    var service = mvc.createService({ owner: 'nobody', app: APP });

    function macroUrl(name) {
        return 'configs/conf-macros/' + encodeURIComponent(name);
    }

    function setStatus(msg, kind) {
        var el = $('#aruba_setup_status');
        el.text(msg);
        el.removeClass('ok err busy').addClass(kind || '');
    }

    // Load the current definition into the input.
    service.get(macroUrl(MACRO), { output_mode: 'json' }, function (err, resp) {
        if (err) { return; }
        try {
            $(FIELD).val(resp.data.entry[0].content.definition || '');
        } catch (e) { /* macro may not exist yet */ }
    });

    function markConfigured() {
        // Flip is_configured so the app no longer shows the setup hint.
        return $.Deferred(function (d) {
            service.post('apps/local/' + APP, { configured: 1 }, function () { d.resolve(); });
        }).promise();
    }

    function refreshCheck() {
        var manager = mvc.Components.get('aruba_verify_search');
        if (manager) { manager.startSearch(); }
    }

    $(document).on('click', '#aruba_setup_save', function () {
        var def = $.trim($(FIELD).val());
        if (!def) {
            setStatus('Enter a search expression, for example index=aruba.', 'err');
            return;
        }
        if (/[|`\r\n]/.test(def)) {
            setStatus('The definition must be a plain search expression. Pipes, backticks and line breaks are not allowed.', 'err');
            return;
        }
        setStatus('Saving\u2026', 'busy');
        service.post(macroUrl(MACRO), { definition: def }, function (err) {
            if (err) {
                setStatus('Save failed. You need write access to the app. You can also edit the macro under Settings \u2192 Advanced search \u2192 Search macros.', 'err');
                return;
            }
            markConfigured().always(function () {
                setStatus('Saved. All dashboards use the new index now.', 'ok');
                refreshCheck();
            });
        });
    });
});
