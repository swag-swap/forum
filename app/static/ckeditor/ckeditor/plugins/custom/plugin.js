CKEDITOR.plugins.add('custom', {
    icons: 'plugin.png', 
    init: function (editor) { 
        editor.addCommand('insertQuestion', {
            exec: function (editor) { 
                var randomId = 'question_' + Math.floor(Math.random() * 1000); 
                var selection = editor.getSelection(); 
                var range = selection.getRanges()[0]; 
                var questionElement = new CKEDITOR.dom.element('div');
                questionElement.setAttribute('id', randomId);
                questionElement.setStyle('margin-bottom', '10px');  
                var buttonElement = new CKEDITOR.dom.element('span');
                buttonElement.setAttribute('id', 'button');
                buttonElement.setText('Click Me'); 
                questionElement.append(buttonElement);

                // Insert the question element at the current cursor position
                range.insertNode(questionElement);

                // Add click event listener to the button
                buttonElement.on('click', function () {
                    // Find the question element by its ID
                    var question = editor.document.getById(randomId);

                    // Check if the question element exists
                    if (question) {
                        var breakElement = new CKEDITOR.dom.element('br');
                        question.append(breakElement);
                        // Create a new div element for the answer
                        var selected = new CKEDITOR.dom.element('input');
                        selected.setAttribute('type', 'radio'); 
                        question.append(selected);
                        var answerElement = new CKEDITOR.dom.element('input');
                        answerElement.setAttribute('type', 'text');
                        answerElement.setAttribute('id', 'answer');
                        answerElement.setAttribute('placeholder','Add options');
                        answerElement.setAttribute('editable', 'true');
                        
                        // Append the answer element to the question
                        question.append(answerElement);
                    } else {
                        console.error('Question element not found for ID:', randomId);
                    }
                });
            }
        });

        // Add toolbar buttons for the commands
        editor.ui.addButton('InsertQuestion', {
            label: 'Insert Question',
            command: 'insertQuestion',
            toolbar: 'insert'
        });
    }
});