arial_16font = pygame.font.SysFont('arial', 16)#(font type, size)

    """--placing the text--"""
    buttons = 'Play Pause Stop Toggle Rew. FF Loop Rev Vis PrevF NextF'.split(' ')
    buttonDict = {}
    leftPoint = 4 #left position of the text
    
    for button in buttons:
        buttonDict[button] = [arial_16font.render(button, True, WHITE, (0,0,0))] #(text, True is for smoothness on text, colour of the text, background color)
        
        buttonDict[button].append(buttonDict[button][0].get_rect())
        pygame.draw.rect(buttonDict[button][0], WHITE, buttonDict[button][1], 1) #(surfae, color, rectangle size, width) if width =0 would be fill with color

        #postion and move the text
        buttonDict[button][1].bottom = HEIGHT - 4 
        buttonDict[button][1].left = leftPoint
        leftPoint += buttonDict[button][1].width + 4

        """
        rect.attributes
        x,y
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, width, height
        w,h
        """

 while True:
            elif event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    if buttonDict[button][1].collidepoint(event.pos): #objects collision with event's position
                        if button == 'Play':
                            anime.play()
                        elif button == 'Pause':
                            anime.pause()
                        elif button == 'Stop':
                            anime.stop()
                        elif button == 'Toggle':
                            anime.togglePause()
                        elif button == 'Rew.':
                            anime.rewind(0.1)
                        elif button == 'FF':
                            anime.fastForward(0.1)
                        elif button == 'Loop':
                            anime.loop = not anime.loop
                        elif button == 'Rev':
                            anime.reverse()
                        elif button == 'Vis':
                            anime.visibility = not anime.visibility
                        elif button == 'PrevF':
                            anime.prevFrame()
                        elif button == 'NextF':
                            anime.nextFrame()

        # draw the animations to the screen
        #anime.currentFrameNum = 3
        #print(anime.currentFrameNum)
        
        for button in buttons:
            screen.blit(buttonDict[button][0], buttonDict[button][1])

        # draw the info text
        stateSurf = arial_16font.render('State: %s' % anime.state, True, WHITE)
        stateRect = stateSurf.get_rect()
        stateRect.topleft = (4, 130)
        screen.blit(stateSurf, stateRect)

        elapsedSurf = arial_16font.render('Elapsed: %s' % anime.elapsed, True, WHITE)
        elapsedRect = elapsedSurf.get_rect()
        elapsedRect.topleft = (150, 130)
        screen.blit(elapsedSurf, elapsedRect)

        curFrameSurf = arial_16font.render('Cur Frame Num: %s' % anime.currentFrameNum, True, WHITE)
        curFrameRect = curFrameSurf.get_rect()
        curFrameRect.topleft = (380, 130)
        screen.blit(curFrameSurf, curFrameRect)

        loopSurf = arial_16font.render('Looping: %s' % anime.loop, True, WHITE)
        loopRect = loopSurf.get_rect()
        loopRect.topleft = (4, 150)
        screen.blit(loopSurf, loopRect)

        visSurf = arial_16font.render('Vis: %s' % anime.visibility, True, WHITE)
        visRect = visSurf.get_rect()
        visRect.topleft = (150, 150)
        screen.blit(visSurf, visRect)

        rightNow = time.time()

        timeSurf = arial_16font.render('Current Time: %s' % rightNow, True, WHITE)
        timeRect = timeSurf.get_rect()
        timeRect.topleft = (4, 170)
        screen.blit(timeSurf, timeRect)

        playTimeSurf = arial_16font.render('Play Start Time: %s' % anime._playingStartTime, True, WHITE)
        playTimeRect = playTimeSurf.get_rect()
        playTimeRect.topleft = (4, 190)
        screen.blit(playTimeSurf, playTimeRect)

        pauseTimeSurf = arial_16font.render('Pause Start Time: %s' % anime._pausedStartTime, True, WHITE)
        pauseTimeRect = pauseTimeSurf.get_rect()
        pauseTimeRect.topleft = (4, 210)
        screen.blit(pauseTimeSurf, pauseTimeRect)

        diffTimeSurf = arial_16font.render('Play - Pause Time: %s' % (anime._playingStartTime - anime._pausedStartTime), True, WHITE)
        diffTimeRect = diffTimeSurf.get_rect()
        diffTimeRect.topleft = (4, 230)
        screen.blit(diffTimeSurf, diffTimeRect)

        diff2TimeSurf = arial_16font.render('Current - Play Time: %s' % (rightNow - anime._playingStartTime), True, WHITE)
        diff2TimeRect = diff2TimeSurf.get_rect()
        diff2TimeRect.topleft = (4, 250)
        screen.blit(diff2TimeSurf, diff2TimeRect)

        diff3TimeSurf = arial_16font.render('Current - Pause Time: %s' % (rightNow - anime._pausedStartTime), True, WHITE)
        diff3TimeRect = diff3TimeSurf.get_rect()
        diff3TimeRect.topleft = (4, 270)
        screen.blit(diff3TimeSurf, diff3TimeRect)
