def aabb_collision(rect1, rect2):
    '''
    Если все четыре условия выполняются, значит, 
    прямоугольники пересекаются, и функция возвращает True. 
    В противном случае, функция возвращает False, указывая на то, 
    что прямоугольники не пересекаются
    '''
    return (rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.y + rect1.height > rect2.y)