CKEDITOR.plugins.add('custom', {
    icons: 'custom',
    init: function (editor) {
        editor.addCommand('insertQuestion', {
            exec: function (editor) {
                // Add logic to insert question field at the current cursor position
                var questionHtml = '<div class="question">Question: <input type="text"></div>';
                editor.insertHtml(questionHtml);
            }
        });

        editor.addCommand('insertAnswer', {
            exec: function (editor) {
                // Add logic to insert answer field at the current cursor position
                var answerHtml = '<div class="answer">Answer: <input type="text"></div>';
                editor.insertHtml(answerHtml);
            }
        });

        editor.ui.addButton('CustomButton', {
            label: 'Custom Button',
            command: 'insertQuestion',
            toolbar: 'insert',
            icon: this.path + 'icons/custom.png'
        });
    }
});
