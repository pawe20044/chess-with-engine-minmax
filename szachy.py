import numpy as np
from copy import deepcopy
class chess:
    def __init__(self):
        self.nrow=8
        self.ncol=8
        self.white_king_moved=False
        self.black_king_moved=False
        self.rook_moved_A1=False
        self.rook_moved_H1=False
        self.rook_moved_A8=False
        self.rook_moved_H8=False
        self.atacked_fields=[]
        self.atacked_fields_black=[]
    def get_initial_state(self):
        state=np.zeros([self.nrow,self.ncol])
        for col in range(self.ncol):
            state[6,col]=1
            state[1,col]=-1
        state[7][0]=5
        state[7][7]=5
        state[7][1]=3
        state[7][6]=3
        state[7][2]=4
        state[7][5]=4
        state[7][3]=9
        state[7][4]= 2 
        state[0][0]=-5
        state[0][7]=-5
        state[0][1]=-3
        state[0][6]=-3
        state[0][2]=-4
        state[0][5]=-4
        state[0][3]=-9
        state[0][4]=-2 
        return state

    def get_valid_moves(self,state,player,atacked,last_move,temp_board):
        moves=[]
        white=[1,2,3,4,5,9]
        black=[-1,-2,-3,-4,-5,-9]
        direct_take=[(-1, -1), (-1, 1)] if player == 1 else [(1, -1), (1, 1)]
        defend=[]
        def make_loop(r,c,direct,player):
            field=5 if player==1 else 2
            for dr in direct:
                nr=r+dr
                difr=abs(nr-r)
                if difr==2:
                    if 0 <= nr < self.nrow and state[nr, c] == 0 and state[field,c]==0:
                      moves.append([(r, c), (nr, c)])
                else:
                    if 0 <= nr < self.nrow and state[nr, c] == 0:
                      moves.append([(r, c), (nr, c)])  
        def make_loop_knight(r,c,directrow,directcol,player):
            for dr in directrow:
                for dc in directcol:
                    nr,nc=r+dr,c+dc
                    color=white if player==1 else black
                    if 0 <= nr < self.nrow and 0 <= nc < self.ncol and state[nr, nc] not in color:
                        moves.append([(r, c), (nr, nc)])
        def make_loop_bishop(r, c, player):
            path = []
            path1 = []
            color = white if player == 1 else black
            reverse_color = black if player == 1 else white
            found=False
            found_1 = False
            found_2 = False
            found_3 = False
            for dr in range(1,8):
                    dc=dr
                    nr, nc, nc1 = r + dr, c + dc, c - dc
                    if not found and  0 <= nr < self.nrow and 0 <= nc < self.ncol:
                        found = check_path(r, c, nr, nc, color, reverse_color)
                        path.append([(r, c), (nr, nc)])
                    if  0 <= nr < self.nrow and 0 <= nc < self.ncol and state[nr,nc] not in color:
                        if [(r, c), (nr, nc)] in path:
                            moves.append([(r, c), (nr, nc)])
                    if not found_1 and  0 <= nr < self.nrow and 0 <= nc1 < self.ncol:
                        found_1 = check_path(r, c, nr, nc1, color, reverse_color)
                        path1.append([(r, c), (nr, nc1)])
                    if  0 <= nr < self.nrow and 0 <= nc1 < self.ncol:
                        if [(r, c), (nr, nc1)] in path1 and state[nr,nc1] not in color:
                            moves.append([(r, c), (nr, nc1)])
            for dr in range(-1,-8,-1):
                    dc=dr
                    nr, nc, nc1 = r + dr, c + dc, c - dc
                    if not found_2 and  0 <= nr < self.nrow and 0 <= nc < self.ncol:
                        found_2 = check_path(r, c, nr, nc, color, reverse_color)
                        path.append([(r, c), (nr, nc)])
                    if  0 <= nr < self.nrow and 0 <= nc < self.ncol and state[nr,nc] not in color:
                        if [(r, c), (nr, nc)] in path:
                            moves.append([(r, c), (nr, nc)])
                    if not found_3 and  0 <= nr < self.nrow and 0 <= nc1 < self.ncol:
                        found_3 = check_path(r, c, nr, nc1, color, reverse_color)
                        path1.append([(r, c), (nr, nc1)])
                    if  0 <= nr < self.nrow and 0 <= nc1 < self.ncol:
                        if [(r, c), (nr, nc1)] in path1 and state[nr,nc1] not in color:
                            moves.append([(r, c), (nr, nc1)])        
        def make_loop_rook(r,c,player):
            color=white if player==1 else black
            reverse_color=black if player==1 else white
            path=[]
            path2=[]
            found=False
            found_2=False
            found_3=False
            found_4=False
            inc=-1 if player==1 else 1
            stop=8 if player==1 else -8
            for dc in range(0,-stop,inc):
                if dc == 0: 
                    continue
                nc=c+dc
                if 0 <= nc < self.nrow:
                    if not found:
                        found=check_path(r,c,r,nc,color,reverse_color)
                        path.append([(r, c), (r, nc)])
                    if [(r, c), (r, nc)] in path and state[r,nc] not in color:
                        moves.append([(r, c), (r, nc)])
            for dc in range(0,stop,-inc):
                if dc == 0: 
                    continue
                nc=c+dc
                if 0 <= nc < self.nrow:
                    if not found_2:
                        found_2=check_path(r,c,r,nc,color,reverse_color)
                        path.append([(r, c), (r, nc)])
                    if [(r, c), (r, nc)] in path and state[r,nc] not in color:
                        moves.append([(r, c), (r, nc)])
                        

            for dr in range(0,-stop,inc):
                if dr == 0: 
                    continue
                nr=r+dr
                if  0 <= nr < self.nrow:
                    if not found_3:
                        found_3=check_path(r,c,nr,c,color,reverse_color)
                        path2.append([(r, c), (nr, c)])
                    if [(r, c), (nr, c)] in path2 and state[nr,c] not in color:
                        moves.append([(r, c), (nr, c)])
            for dr in range(0,stop,-inc):
                if dr == 0: 
                    continue
                nr=r+dr
                if  0 <= nr < self.nrow:
                    if not found_4:
                        found_4=check_path(r,c,nr,c,color,reverse_color)
                        path2.append([(r, c), (nr, c)])
                    if [(r, c), (nr, c)] in path2 and state[nr,c] not in color:
                        moves.append([(r, c), (nr, c)])
                        
        def check_pawn_take(r,c,direct,player):
                 color=black if player==1 else white
                 for dr, dc in direct:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.nrow and 0 <= nc< self.nrow and state[nr,nc] in color:
                        moves.append([(r, c), (nr, nc)])
        def make_loop_king(r,c,player):
            color=black if player==1 else white
            for dr in range(-1,2):
                for dc in range(-1,2):
                    nr=r+dr
                    nc=c+dc
                    if 0 <= nr < self.nrow and (state[nr,c] in color or state[nr,c]==0 ) and [nr,c] not in atacked:
                        moves.append([(r, c), (nr, c)])
                    if 0 <= nc < self.nrow and (state[r,nc] in color or state[r,nc]==0) and [r,nc] not in atacked :
                        moves.append([(r, c), (r, nc)])
                    if 0 <= nc < self.nrow and  0 <= nr < self.nrow  and (state[nr,nc] in color or state[nr,nc]==0) and [nr,nc] not in atacked:
                        moves.append([(r, c), (nr, nc)])
        def check_path(r,c,nr,nc,color,reverse_color):
            if state[nr][nc] in color:
                defend.append([(r, c), (nr, nc)])
                return True
            elif state[nr][nc] in reverse_color:
                moves.append([(r, c), (nr, nc)])
                return True
            return False

        def check_castle(r,c,player):
            king_moved=self.white_king_moved if player==1 else self.black_king_moved
            rook_moved_short=self.rook_moved_H1 if player==1 else self.rook_moved_H8
            rook_moved_long=self.rook_moved_A1 if player==1 else self.rook_moved_A8
            short_catle=True
            long_castle=True
            if (r,5) not in atacked and (r,6) not in atacked:
                short_catle=False
            if (r,1) not in atacked and (r,2) not in atacked and (r,3) not in atacked:
                long_castle=False
            if state[r,c]==2*player and king_moved==False and rook_moved_short==False and state[r,5]==0 and state[r,6]==0 and short_catle:
                moves.append([(r, c), (r, 6),(r, 7), (r, 5)])
            if state[r,c]==2*player and king_moved==False and rook_moved_long==False and state[r,1]==0 and state[r,2]==0 and state[r,3]==0 and long_castle:
                moves.append([(r, c), (r, 2),(r, 0), (r, 3)])
        def en_passant(state,move,moves):
            (r,c),(r1,c1)=move
            player=state[r1,c1]
            difr=abs(r-r1)
            if 0<c1-1:
                if player ==-1 and difr==2 and state[r1,c1-1]==-player:
                    moves.append([(r1,c1-1),(r1-1,c1)])
                elif player==1 and difr==2 and state[r1,c1-1]==-player:
                    moves.append([(r1,c1-1),(r1+1,c1)])
            if c1+1<self.ncol:
                if player==1 and difr==2 and state[r1,c1+1]==-player:
                    moves.append([(r1,c1+1),(r1+1,c1)])
                elif player==-1 and difr==2 and state[r1,c1+1]==-player and c1+1<self.ncol:
                    moves.append([(r1,c1+1),(r1-1,c1)])
        def find_possible_moves(state, moves, player):
            valid_moves = [] 
            for move in moves:
                temp_state = deepcopy(state)
                new_state = self.move(move, temp_state)
                king_pos = find_king(player, new_state)
        
                your_moves,your_defend = self.get_valid_moves(new_state, player, atacked, move , temp_board=True)
                your_atacked = self.get_atacked_fields(new_state, your_moves,your_defend, player)
                enemy_moves,enemy_defend = self.get_valid_moves(new_state, -player, your_atacked, move, temp_board=True)
                enemy_atacked = self.get_atacked_fields(new_state, enemy_moves,enemy_defend, -player)
        
                if king_pos not in enemy_atacked: 
                    valid_moves.append(move)
            return valid_moves
        def find_king(player,state):
            for r in range(self.nrow):
                for c in range(self.ncol):
                    if state[r,c]==2*player:
                        return [r,c]
        for r in range(self.nrow):
            for c in range(self.ncol):
                 if state[r][c]==player and r==6 and player==1: 
                    direct=[-1,-2]
                    make_loop(r,c,direct,player)
                    check_pawn_take(r,c,direct_take,player)
                 elif state[r][c]==player and r==1 and player==-1:
                    direct=[1,2]
                    make_loop(r,c,direct,player)
                    check_pawn_take(r,c,direct_take,player)
                 elif state[r][c]==player:
                    direct=[-1] if player==1 else [1]
                    make_loop(r,c,direct,player)
                    check_pawn_take(r,c,direct_take,player)
                 if state[r][c]==3*player:
                    directrow=[2,-2]
                    directcol=[1,-1]
                    directrow1=[1,-1]
                    directcol1=[2,-2]
                    make_loop_knight(r,c,directrow,directcol,player)
                    make_loop_knight(r,c,directrow1,directcol1,player)
                 if state[r][c]==4*player:
                    make_loop_bishop(r,c,player)
                 if state[r][c]==5*player:
                    make_loop_rook(r,c,player)
                 if state[r][c]==9*player:
                    make_loop_rook(r,c,player)
                    make_loop_bishop(r,c,player)
                 if state[r][c]==2*player:
                    make_loop_king(r,c,player)
                    check_castle(r,c,player)
        if last_move is not None:
            en_passant(state,last_move,moves)
        if temp_board==False:
            moves=find_possible_moves(state,moves,player)
        return moves,defend
    def move(self,move,state):
        if len(move)==2:
            (r,c),(r1,c1)=move
            player=state[r,c]
            self.is_en_passant(state,move)
            self.if_moved(player,r,c)
            state[r,c]=0
            state[r1,c1]=player
            
        else:
            (r,c),(r1,c1),(r2,c2),(r3,c3)=move
            player=state[r,c]
            state[r,c]=0
            state[r1,c1]=player
            player2=state[r2,c2]
            state[r2,c2]=0
            state[r3,c3]=player2
        return state
    def if_moved(self,player,r,c):
        if player==2:
            self.white_king_moved=True
        elif player==-2:
            self.black_king_moved=True
        if player==5 and r==7:
            if c==0:
                self.rook_moved_A1=True
            else:
                self.rook_moved_H1=True
        if player==-5 and r==0:
            if c==0:
                self.rook_moved_A8=True
            else:
                self.rook_moved_H8=True
    def is_en_passant(self,state,move):
        (r,c),(r1,c1)=move
        player=state[r,c]
        if player==1 and state[r1,c1]==0 and state[r1+1,c1]==-player:
            state[r1+1,c1]=0
        elif player==-1 and state[r1,c1]==0 and state[r1-1,c1]==-player:
            state[r1-1,c1]=0
    def get_atacked_fields(self,state,moves,defend,player):
        moves=moves+defend
        atacked=[]
        dr=-1 if player==1 else 1
        for move in moves:
            if len(move)==2:
                (r,c),(rr,cc)=move
                if state[r,c]!=player:
                    atacked.append([rr,cc])
        for r in range(self.nrow):
            for c in range(self.ncol):
                if state[r,c]==player:
                    atacked.append([r+dr,c+1])
                    atacked.append([r+dr,c-1])
        return atacked
    def check_mate(self,state,moves,atacked,player):
        pos=self.find_king_1(player,state)
        if len(moves)==0 and pos in atacked:
            state=self.get_initial_state()
            return state
        elif len(moves)==0:
            print('Draw')
            state=self.get_initial_state()
            return state
        return state
    def find_king_1(self,player,state):
            for r in range(self.nrow):
                for c in range(self.ncol):
                    if state[r,c]==2*player:
                        return [r,c]
import pygame
import numpy as np


pygame.init()


WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")


pieces_images = {
    1: pygame.image.load("white-pawn.png"),
    -1: pygame.image.load("black-pawn.png"),
    5: pygame.image.load("white-rook.png"),
    -5: pygame.image.load("black-rook.png"),
    3: pygame.image.load("white-knight.png"),
    -3: pygame.image.load("black-knight.png"),
    4: pygame.image.load("white-bishop.png"),
    -4: pygame.image.load("black-bishop.png"),
    9: pygame.image.load("white-queen.png"),
    -9: pygame.image.load("black-queen.png"),
    2: pygame.image.load("white-king.png"),
    -2: pygame.image.load("black-king.png"),
}


for key in pieces_images:
    pieces_images[key] = pygame.transform.scale(pieces_images[key], (100, 100))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (118, 150, 86)
LIGHT_BROWN = (238, 238, 210)
GREY = (128, 128, 128)
SQUARE_SIZE = WIDTH // 8

def draw_board():    
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(SCREEN, color, pygame.Rect(col * 100, row * 100, 100, 100))

def draw_pieces(state):
    for row in range(8):
        for col in range(8):
            piece = state[row][col]
            if piece != 0:
                SCREEN.blit(pieces_images[piece], (col * 100, row * 100))
def highlight_moves(win, moves, selected_piece):
    for move in moves:
        if move[0] == selected_piece:  
            if len(move)==2:
                (r, c) = move[-1]  
                pygame.draw.circle(win, GREY, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10, width=5)
            else:
                (r, c) = move[1]  
                pygame.draw.circle(win, GREY, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10, width=5)

def promote_pawn_screen(screen, player):
    if player==1:
        queen_img = pygame.image.load('white-queen.png')
        rook_img = pygame.image.load('white-rook.png')
        knight_img = pygame.image.load('white-knight.png')
        bishop_img = pygame.image.load('white-bishop.png')
    else:
        queen_img = pygame.image.load('black-queen.png')
        rook_img = pygame.image.load('black-rook.png')
        knight_img = pygame.image.load('black-knight.png')
        bishop_img = pygame.image.load('black-bishop.png')
    
   
    queen_rect = queen_img.get_rect(topleft=(330, 100))
    rook_rect = rook_img.get_rect(topleft=(330, 250))
    knight_rect = knight_img.get_rect(topleft=(330, 400))
    bishop_rect = bishop_img.get_rect(topleft=(330, 550))
    
   
    draw_board()
    screen.blit(queen_img, queen_rect)
    screen.blit(rook_img, rook_rect)
    screen.blit(knight_img, knight_rect)
    screen.blit(bishop_img, bishop_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if queen_rect.collidepoint(mouse_pos):
                    return 9 * player
                elif rook_rect.collidepoint(mouse_pos):
                    return 5 * player  
                elif knight_rect.collidepoint(mouse_pos):
                    return 3 * player  
                elif bishop_rect.collidepoint(mouse_pos):
                    return 4 * player  

def promote(state, row, col, promote_row, player, screen):
    if state[row, col] == player and row == promote_row:
        promoted_piece = promote_pawn_screen(screen, player)
        state[row, col] = promoted_piece
    return state
def main():
    game = chess()
    clock = pygame.time.Clock()
    state = game.get_initial_state()
    running = True
    player_turn = 1
    lastmove=None
    atacked=[]
    moves_enemy,defend=game.get_valid_moves(state,-player_turn,atacked,lastmove,temp_board=False)
    atacked_fields=game.get_atacked_fields(state,moves_enemy,defend,-player_turn)
    valid_moves,_ = game.get_valid_moves(state, player_turn,atacked_fields,lastmove,temp_board=False)
    selected_piece = None
    promote_row=0 if player_turn==1 else 7
    while running:
        SCREEN.fill(WHITE)
        draw_board()
        draw_pieces(state)
        chain_valid_moves=[]
        for move in valid_moves:
            if len(move)>2:
                chain_valid_moves.append(move)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
            
                if selected_piece:
                    move = [selected_piece, (row, col)]
                    if chain_valid_moves:
                        for chain_move in chain_valid_moves:
                            (r,c),(r1,c1)=chain_move[0],chain_move[1]
                            if move==[(r,c),(r1,c1)]:
                                move=chain_move
                    if move in valid_moves:
                        state = game.move(move, state)
                        state=promote(state,row,col,promote_row,player_turn,SCREEN)
                        lastmove=move
                        selected_piece = None
                        player_turn = -player_turn
                        moves_enemy,defend=game.get_valid_moves(state,-player_turn,atacked_fields,lastmove,temp_board=False)
                        atacked_fields=game.get_atacked_fields(state,moves_enemy,defend,-player_turn)
                        valid_moves,_ = game.get_valid_moves(state, player_turn,atacked_fields,lastmove,temp_board=False)
                        state=game.check_mate(state,valid_moves,atacked_fields,player_turn)
                    else:
                        selected_piece = None 
                else:
                    if state[row][col] * player_turn > 0: 
                        selected_piece = (row, col)
                        valid_moves,_ = game.get_valid_moves(state, player_turn,atacked_fields,lastmove,temp_board=False)
        if selected_piece:
            highlight_moves(SCREEN, valid_moves, selected_piece)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()