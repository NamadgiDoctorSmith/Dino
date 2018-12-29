from copy import deepcopy

class tileEdge :
    def __init__(self, color, half):
        self.color = color
        self.half = half


class Tile:

    def __init__(self, id, edges):
        self.id = id
        self.edges = edges
        self.boardPos = None

    def edgeString(self):
        s = ''
        for e in self.edges:
            s = s + e.color + str(e.half) + ','
        return s

    def getId( self ):
        return self.id

    def dump(self, rotation ):
        print( "Tile", self.id, self.edgeString(), rotation )

    def setBoardPos(self, pos):
        self.boardPos = pos

    def getBoardPos(self):
        return self.boardPos

    def edge( self, whichEdge, rotation):
        if (whichEdge=='T'): return self.edges[(0+rotation) % 4]
        if (whichEdge=='R'): return self.edges[(1+rotation) % 4]
        if (whichEdge=='B'): return self.edges[(2+rotation) % 4]
        if (whichEdge=='L'): return self.edges[(3+rotation) % 4]

class Tiles:

    def __init__(self, tiles):
        self.tiles = tiles

    def getTiles( self ):
        return self.tiles

    def dump(self):
        for tile in self.tiles:
            tile.dump(0)

    def getTile( self, pos):
        return self.tiles[pos]

    def removeTile( self, pos):
        self.tile = self.getTile( pos )
        self.tiles[pos] = None
        return self.tile

    def getTilePos( self, tile ):
        for thisTile in self.tiles:
            if (thisTile == tile):
                return thisTile.key

    def getNextFreeTile( self ):
        for tile in self.tiles:
            if (tile.getBoardPos is not None):
                return tile
        return None

class Board:
    def __init__(self):
        self.tiles = [ None, None, None, None, None, None, None, None, None]
        self.rotations = [0,0,0,0,0,0,0,0,0]

    def dump(self):
        print( "/nBoard")
        for tile in self.tiles:
            if (tile is not None): 
                tile.dump( self.rotations[tile.getBoardPos()] )
            else : 
                print( 'None')

    def rotateTile(self, boardpos):
        self.rotations[boardpos] = self.rotations[boardpos] + 1

    def compareTiles( self, t1, t2, edge1, edge2 ):
        if ((t1 is None) or (t2 is None)):
            return True
        else:
            return self.compareEdges( 
                t1.edge(edge1, self.rotations[t1.getBoardPos()]), 
                t2.edge(edge2, self.rotations[t2.getBoardPos()]))

    def compareEdges( self, e1, e2):
        # the color must be the same
        if (e1.color == e2.color) :
            if (e1.half != e2.half) :
                return True
        return False


    def ok(self, pos):
        # test to see if the tile just placed into pos is ok with all other tiles in the board

        res = True
        # is the tile NOT on a left most edge
        if ((pos % 3) != 0):
            # check that the left edge of this tile matches the right edge of the left one
            if (not self.compareTiles( self.tiles[pos], self.tiles[pos-1], 'L', 'R' )):
                res = False

        if (res == True):
            # is the tile NOT on a right most edge
            if ((pos % 3) != 2):
                # check that the left edge of this tile matches the right edge of the left one
                if (not self.compareTiles( self.tiles[pos], self.tiles[pos+1], 'R', 'L' )):
                    res = False

            if (res == True):
                # is the tile NOT on a top most edge
                if (pos>2):
                    # check that the left edge of this tile matches the right edge of the left one
                    if (not self.compareTiles( self.tiles[pos], self.tiles[pos-3],'T', 'B')):
                        res = False

                if (res == True):
                    # is the tile NOT on a bottom most edge
                    if (pos<6):
                        # check that the bottom edge of this tile matches the top edge of the other
                        if (not self.compareTiles( self.tiles[pos], self.tiles[pos+3], 'B', 'T')):
                            res = False
        return res

    def setTile( self, pos, tile, rotation):
        self.tiles[pos] = tile
        self.rotations = rotation
        tile.setBoardPos(pos)
        return self.ok(pos)


    # this is the main recursive function, it attempts to select and then place a tile 
    # onto the board, if it runs out of free tiles then it has solved the puzzle
    # otherwise is recursively tries all possible combinations.  It creates a local
    # deep copy of the board and the tileset at each recursion

    def placeTile( self, tiles, board, boardPos, depth):
        # create a local copy of the board and the tiles

        #print( "Start scan at depth =", depth )

        localTiles = deepcopy(tiles)
        localBoard = deepcopy(board)

        # scan over the free tiles

        noTilesLeft = True
        for freeTile in localTiles.getTiles():

            if (freeTile.getBoardPos() is None) :


                noTilesLeft = False
                # place a specified tile on the board after removing it from the free tiles
                freeTile.setBoardPos( boardPos )
                localBoard.tiles[boardPos] = freeTile

                for rotation in [0,1,2,3]:
                    if (depth==0):
                        print( 'Depth=', depth, 'Tile=', freeTile.id, 'board pos=', boardPos, "rot=", rotation )
                    # set the rotation
                    localBoard.rotations[boardPos] = rotation
                    # if it is ok then recursively try another tile
                    if (localBoard.ok(boardPos)):
                        #print( 'Matched board so far !')
                        #localBoard.dump()
                        localBoard.placeTile( localTiles, localBoard, boardPos+1, depth+1)

                # get to here means that the tile didn't match or we have a solution

                freeTile.setBoardPos( None )

        # if we simple fell through because there are no more tiles then we have solved it
        if (noTilesLeft == True):
            print( "**************** SOLUTION ****************")
            localBoard.dump()
            exit
            return True
        else:
            #print( "no solution this way ...")
            return False

print( "Dinosaur Puzzle Solver")

tiles = Tiles( 
    [
    Tile( 1, [ tileEdge( 'G', 'B'), tileEdge( 'O', 'F'), tileEdge('O','B'), tileEdge('B','F')]),
    Tile( 2, [ tileEdge( 'O', 'F'), tileEdge( 'N', 'B'), tileEdge('G','B'), tileEdge('B','B')]),
    Tile( 3, [ tileEdge( 'N', 'F'), tileEdge( 'G', 'B'), tileEdge('B','F'), tileEdge('O','F')]),
    Tile( 4, [ tileEdge( 'N', 'F'), tileEdge( 'G', 'B'), tileEdge('G','F'), tileEdge('B','B')]),
    Tile( 5, [ tileEdge( 'B', 'F'), tileEdge( 'N', 'B'), tileEdge('O','B'), tileEdge('G','F')]),
    Tile( 6, [ tileEdge( 'B', 'F'), tileEdge( 'G', 'F'), tileEdge('N','F'), tileEdge('O','F')]),
    Tile( 7, [ tileEdge( 'B', 'F'), tileEdge( 'N', 'B'), tileEdge('O','F'), tileEdge('N','F')]),
    Tile( 8, [ tileEdge( 'B', 'F'), tileEdge( 'O', 'F'), tileEdge('N','F'), tileEdge('G','F')]),
    Tile( 9, [ tileEdge( 'B', 'B'), tileEdge( 'G', 'B'), tileEdge('N','B'), tileEdge('O','B')]),
    ]
)

board = Board()

print( board.placeTile( tiles, board, 0, 0 ))

#print( tiles.dump())
#print ( board.dump())
