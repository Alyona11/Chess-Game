$(document).ready(function() {
    isWhiteTurn = true

    var chessboard = '<div class="numbering number">8</div>' +
                     '<div class="square white a8">♜</div>' +
                     '<div class="square black b8">♞</div>' +
                     '<div class="square white c8">♝</div>' +
                     '<div class="square black d8">♛</div>' +
                     '<div class="square white e8">♚</div>' +
                     '<div class="square black f8">♝</div>' +
                     '<div class="square white g8">♞</div>' +
                     '<div class="square black h8">♜</div>' +
                     '<div class="numbering number">7</div>' +
                     '<div class="square black a7">♟</div>' +
                     '<div class="square white b7">♟</div>' +
                     '<div class="square black c7">♟</div>' +
                     '<div class="square white d7">♟</div>' +
                     '<div class="square black e7">♟</div>' +
                     '<div class="square white f7">♟</div>' +
                     '<div class="square black g7">♟</div>' +
                     '<div class="square white h7">♟</div>' +
                     '<div class="numbering number">6</div>' +
                     '<div class="square white a6"></div>' +
                     '<div class="square black b6"></div>' +
                     '<div class="square white c6"></div>' +
                     '<div class="square black d6"></div>' +
                     '<div class="square white e6"></div>' +
                     '<div class="square black f6"></div>' +
                     '<div class="square white g6"></div>' +
                     '<div class="square black h6"></div>' +
                     '<div class="numbering number">5</div>' +
                     '<div class="square black a5"></div>' +
                     '<div class="square white b5"></div>' +
                     '<div class="square black c5"></div>' +
                     '<div class="square white d5"></div>' +
                     '<div class="square black e5"></div>' +
                     '<div class="square white f5"></div>' +
                     '<div class="square black g5"></div>' +
                     '<div class="square white h5"></div>' +
                     '<div class="numbering number">4</div>' +
                     '<div class="square white a4"></div>' +
                     '<div class="square black b4"></div>' +
                     '<div class="square white c4"></div>' +
                     '<div class="square black d4"></div>' +
                     '<div class="square white e4"></div>' +
                     '<div class="square black f4"></div>' +
                     '<div class="square white g4"></div>' +
                     '<div class="square black h4"></div>' +
                     '<div class="numbering number">3</div>' +
                     '<div class="square black a3"></div>' +
                     '<div class="square white b3"></div>' +
                     '<div class="square black c3"></div>' +
                     '<div class="square white d3"></div>' +
                     '<div class="square black e3"></div>' +
                     '<div class="square white f3"></div>' +
                     '<div class="square black g3"></div>' +
                     '<div class="square white h3"></div>' +
                     '<div class="numbering number">2</div>' +
                     '<div class="square white a2">♙</div>' +
                     '<div class="square black b2">♙</div>' +
                     '<div class="square white c2">♙</div>' +
                     '<div class="square black d2">♙</div>' +
                     '<div class="square white e2">♙</div>' +
                     '<div class="square black f2">♙</div>' +
                     '<div class="square white g2">♙</div>' +
                     '<div class="square black h2">♙</div>' +
                     '<div class="numbering number">1</div>' +
                     '<div class="square black a1">♖</div>' +
                     '<div class="square white b1">♘</div>' +
                     '<div class="square black c1">♗</div>' +
                     '<div class="square white d1">♕</div>' +
                     '<div class="square black e1">♔</div>' +
                     '<div class="square white f1">♗</div>' +
                     '<div class="square black g1">♘</div>' +
                     '<div class="square white h1">♖</div>' +
                     '<div class="numbering placeholder"></div>' +
                     '<div class="numbering letter">a</div>' +
                     '<div class="numbering letter">b</div>' +
                     '<div class="numbering letter">c</div>' +
                     '<div class="numbering letter">d</div>' +
                     '<div class="numbering letter">e</div>' +
                     '<div class="numbering letter">f</div>' +
                     '<div class="numbering letter">g</div>' +
                     '<div class="numbering letter">h</div>';

    // Викноується при натисканні на елемент з класом 'save', тобто при натисканні на кнопку 'Save'
    $('.save').click(function(e) {
        $.post('/save') // Надсилається POST реквест на localhost:5000/save
    });

    // Викноується при натисканні на елемент з класом 'new', тобто при натисканні на кнопку 'New Game'
    $('.new').click(function(e) {
        $.post('/new', function(response) { // Надсилається POST реквест на localhost:5000/new
            isWhiteTurn = true
            $('.player')[0].innerHTML = '♔' // Виставити наступний хід білим фігурам
            $('.chessboard')[0].innerHTML = chessboard // Виставити фігури в початкові позиції
        })
    })

    // Викноується при натисканні на елемент з класом 'square', тобто при натисканні на будь-яку клітинку дошки
    $('.square').click(function(e) {
        if($(this).hasClass('target')) { // Якщо клітинка є клтинкою для виконання ходу
            position = $('.position')[0]
            $.post('/movement', { // Виконати хід на клітинку
                    'position': position.className.split(' ')[2],
                    'target': e.target.className.split(' ')[2]
                },
                function(response) {
                    if(response.isCheckmate == true) { // Перевірити, чи є мат
                        $('.message')[0].innerHTML = 'Checkmate!' // Показати повідомлення про мат
                    } else if (response.isCheck == true) { // Перевірити, чи є шах
                        $('.message')[0].innerHTML = 'Check!' // Показати повідомлення про шах
                    }
                    e.target.innerHTML = position.innerHTML // Переставити фігуру на нову позицію
                    position.innerHTML = '' // Очистити стару позицію
                    isWhiteTurn = !isWhiteTurn // Змінити поточного гравця
                    if(isWhiteTurn == true) {
                        $('.player')[0].innerHTML = '♔'
                    } else {
                        $('.player')[0].innerHTML = '♚'
                    }
                }
            )
            $('.square').removeClass('target')
            $('.square').removeClass('position')
        } else if(e.target.innerHTML !== '') { // Якщо клітинка не порожня
            $('.square').removeClass('target')
            $('.square').removeClass('position')
            $(this).addClass('position') // Позначити клітинку класом 'position'
            $.post('/targets', {'position': e.target.className.split(' ')[2]}, // Вирахувати всі можливі клітинки для ходу
                function(data) {
                    for (i = 0; i < data.targets.length; i++) { // Позначити всі можливі кліинки для ходу класом 'target'
                        $('.' + data.targets[i]).addClass('target')
                    }
                }
            ).fail(function(error) { // Показати повідомлення про помилку, отримане від сервера
                $('.message')[0].innerHTML = error.responseJSON
                $('.message').fadeIn();
                $('.message').fadeOut(3000);
            });
        }
    });
});