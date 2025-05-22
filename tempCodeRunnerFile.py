
    screen.fill(background_color)
    show_countdown1(screen, font_bigtext, background_color, clock)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        title_running = False