$(document).ready(() => {
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;

        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }
    function cloneMore(selector, prefix) {
        let newElement = $(selector).clone(true);
        let total = $('#id_' + prefix + '-TOTAL_FORMS').val();

        newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
            let name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
            let id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });

        newElement.find('td').each(function() {
            let name = $(this).attr('id').replace('-' + (total-1) + '-', '-' + total + '-');
            let id = 'id_' + name;
            $(this).attr({'id': id}).val('').removeAttr('checked');
        });

        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);

        return false;
    }

    function deleteForm(prefix) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1){
            $(".author-form:last").remove();
            let forms = $('.author-form');

            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (let i=0, formCount=forms.length; i<formCount; i++) {
                $(forms.get(i)).find('td').each(function() {
                    updateElementIndex(this, prefix, i);
                });
            }
        } else {
            alert("Ops... Siapa yang punya karya?");
        }
        return false;
    }

    $(document).on("click", "#add-author", (e) => {
        e.preventDefault();
        cloneMore(".author-form:last", 'form');
        return false;
    });

    $(document).on("click", "#remove-author", (e) => {
        e.preventDefault();
        deleteForm('form');
        return false;
    });

});

