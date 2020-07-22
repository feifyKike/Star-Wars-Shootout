# game_functions.py
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from asteroid import Asteroid

def check_events(ai_settings, screen, stats, sb, play_button, ship,
                 aliens, bullets):
    """Responding to user input events"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  
                pygame.quit() # Deactivate program attributes
                sys.exit() # Close the window

            if event.key == pygame.K_UP:
                ship.moving_up = True

            elif event.key == pygame.K_DOWN:
                ship.moving_down = True

            elif event.key == pygame.K_SPACE: # checks for the press of space bar
                # Create a new bullet and add it to the bullets group.
               if len(bullets) < ai_settings.bullets_allowed:
                    new_bullet = Bullet(ai_settings, screen, ship)
                    bullets.add(new_bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ship.moving_up = False
            elif event.key == pygame.K_DOWN:
                ship.moving_down = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start a new game when the player presses the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor once clicked
        ####

        # Reset the game statistics.
        stats.reset_stats() # -> take out highscore from this setting to keep it
        stats.game_active = True

        # Reset the score + level
        sb.prep_score()
        sb.prep_level()
        sb.prep_lives()

        # Prep the last games high score
        sb.prep_high_score()
        
        # Empty the list of old aliens, bullets, and asteroids
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
            

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, asteroids):
    """Doing screen updates on all screen surfaces"""
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Draw a ship
    ship.blitme()

    # Draw the asteroids
    for asteroid in asteroids.sprites():
        asteroid.blitme()

    # Draw the fleet of aliens 
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button() 

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                   bullets, asteroids):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet position
    bullets.update()

    # Getting the screen rect of the right side
    screen_rect = screen.get_rect()
    
    for bullet in bullets.copy():
        if bullet.rect.left >= screen_rect.right:
            bullets.remove(bullet)

    # Check for any bullets that have collided with the aliens
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets, asteroids)

def check_bullet_alien_collisions(ai_settings, screen, stats,
                                  sb, ship, aliens, bullets, asteroids):
    """Responding to bullet collisions with aliens"""
    # If so, get rid of the bullet + alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # the 2 True statements say whether we want either item to disappear

    # Giving points for collisions
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # checking if the alien fleet has diminished
    if len(aliens) == 0:
        # Destroy the existing bullets, speed up game, and create new fleet of aliens
        bullets.empty()
        ai_settings.increase_speed()

        # Start a new level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

        # Check level to initiate the asteroid spawn
        #if stats.level == 3:
        create_asteroid_belt1(ai_settings, screen, asteroids)
        

def check_high_score(stats, sb):
    """Check to see if the current score is larger then the highscore"""
    if stats.score > int(stats.high_score):
        stats.high_score = stats.score
        store_high_score(stats)
        sb.prep_high_score()

def store_high_score(stats):
    """Save the highscore in the json module + relay back"""
    filename = 'high_score_store.txt'
    with open(filename, 'w') as file:
        file.write(str(stats.high_score))

def get_number_aliens_y(ai_settings, alien_height):
    """Determine the number of aliens that fit in a row"""
    available_space_y = ai_settings.screen_height - (2 * alien_height) 
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y

# New function to find the number of columns
def get_number_columns(ai_settings, ship_width, alien_width):
    """Determining the number of columns that fit on screen"""
    available_space_x = (ai_settings.screen_width -
                         (3 * alien_width) - ship_width)
    number_columns = int(available_space_x / (2.5 * alien_width))
    return number_columns

def create_alien(ai_settings, screen, aliens, alien_number, column_number):
    alien = Alien(ai_settings, screen)
    alien_height = alien.rect.height
    alien.y = alien_height + 2 * alien_height * alien_number 
    alien.rect.y = alien.y
    
    # Code addition for the rows and position of each new column
    # -------PROBLEM--------- #
    alien.x = alien.rect.width + 2 * alien.rect.width * (3.5 - column_number)
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_y = get_number_aliens_y(ai_settings, alien.rect.height)

    # New addition to create fleet
    number_columns = get_number_columns(ai_settings, ship.rect.width, alien.rect.width)
    
    # Create the fleet of aliens
    for column_number in range(number_columns):
        for alien_number in range(number_aliens_y):
            create_alien(ai_settings, screen, aliens, alien_number, column_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond if the aliens reach the edge of the window"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Move the fleet slowly to the left and change its direction"""
    for alien in aliens.sprites():
        alien.rect.x -= ai_settings.fleet_slide_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, asteroids):
    """Respond to ship collision"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Show new amount of lives
        sb.prep_lives()
    else:
        stats.game_active = False


    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    asteroids.empty()

    # Create a new fleet, new set of asteroids, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    create_asteroid_belt1(ai_settings, screen, asteroids)
    ship.center_ship()

    # Create a pause after collision
    sleep(0.5)

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, asteroids):
    """
    Check if the fleet is at the edge and then
    update the positions of each
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien collisions with the ship
    if pygame.sprite.spritecollideany(ship, aliens):            
        ship_hit(ai_settings, stats, sb, screen, ship, aliens,
                 bullets, asteroids)

def create_asteroid_belt1(ai_settings, screen, asteroids):
    ast = Asteroid(ai_settings, screen)
    asteroids.add(ast)

def create_asteroid_belt2(ai_settings, screen, asteroids):
    for asteroid in asteroids.copy():
        screen_rect = screen.get_rect()
        if asteroid.rect.centerx == screen_rect.centerx:
            create_asteroid_belt1(ai_settings, screen, asteroids)
            

def update_asteroid(ai_settings, stats, sb, screen,
                    ship, aliens, bullets, asteroids):
    asteroids.update()

    check_ship_asteroid_collisions(ai_settings, stats, sb,
                                   screen, ship, aliens, bullets, asteroids)
    
    for asteroid in asteroids.copy():
        if asteroid.rect.right < 0:
            asteroids.remove(asteroid)
            

def check_ship_asteroid_collisions(ai_settings, stats, sb,
                                   screen, ship, aliens, bullets, asteroids):
    """Check for if the asteroids collided or not"""
    ast_collisions = pygame.sprite.spritecollideany(ship, asteroids)
    if ast_collisions:
        ship_hit(ai_settings, stats, sb, screen, ship, aliens,
                 bullets, asteroids)
        create_asteroid_belt2(ai_settings, screen, asteroids)
    else:
        create_asteroid_belt2(ai_settings, screen, asteroids)
        

    
        
    
    

    
        







    
                          
