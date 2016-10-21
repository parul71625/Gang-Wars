import string
import copy

class TreeNode(object):
    def __init__(self, nodeName, parent, data, utilityValue, moveType, positionOnBoard, depthOfTree):
        self.nodeName = nodeName
        self.data = data
        self.utilityValue =  utilityValue
        self.moveType = moveType
        self.parent = parent
        self.positionOnBoard = positionOnBoard
        self.depthOfTree = depthOfTree
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



class homework2:

   matrixSize = 0
   algo = ""
   player = ""
   oppPlayer = ""
   depth = 0
   adjacencyMatrix = []

   def createGameBoard(self, lineNoToRead):
        lineCount = 0
        with open('input.txt') as inputFile:
            for line in inputFile:
                if not line or line.isspace():
                    continue
                if lineCount == lineNoToRead-2:
                    break
                lineCount += 1

            for line in inputFile:
                if not line or line.isspace():
                    continue
                if lineCount < lineNoToRead - 2 + self.matrixSize:
                    line = line.replace('\n',"")
                    boardValues = line.split(" ")
                    rowList = []
                    for value in boardValues:
                         valuesList = [value,"~"]
                         rowList.append(valuesList)
                    self.adjacencyMatrix.append(rowList)
                    lineCount += 1

                if lineCount == lineNoToRead - 2 + self.matrixSize:
                    index = 0
                    for line in inputFile:
                        if not line or line.isspace():
                            continue
                        #print(line)
                        line = line.replace('\n', "")
                        listOfValues = self.adjacencyMatrix[index]
                        innerIndex = 0
                        for character in line:
                            boardValueList = listOfValues[innerIndex]
                            if character == "X":
                                boardValueList[1] = "X"
                            if character == "O":
                                boardValueList[1] = "O"
                            listOfValues[innerIndex] = boardValueList
                            innerIndex += 1
                        self.adjacencyMatrix[index] = listOfValues
                        index += 1
            #print(self.adjacencyMatrix, "\n")



   def readInputFileAndCreateMatrix(self):
        count = 1
        endOfBoardValue = 0
        inputFile = open('input.txt', 'r')
        for line in inputFile.readlines():
            if not line or line.isspace():
                continue
            if count == 1:
                self.matrixSize = int(line)
            if count == 2:
                line = line.replace('\n', "")
                self.algo = line
            if count == 3:
                line = line.replace('\n', "")
                self.player = line
                if(self.player == "X"):
                    self.oppPlayer = "O"
                else:
                    self.oppPlayer = "X"
            if count == 4:
                self.depth = int(line)
            if count == 5:
                self.createGameBoard(count)
            count += 1



   def calculateBoardValue(self,adjMatrix):
       sumOfX = 0
       sumOfO = 0
       totalSum = 0
       for index in range(0, self.matrixSize):
           rowInMatrix = adjMatrix[index]
           for innerIndex in range(0,len(rowInMatrix)):
               boardValue = rowInMatrix[innerIndex]
               if(boardValue[1] == "X"):
                   sumOfX += int(boardValue[0])
               if (boardValue[1] == "O"):
                   sumOfO += int(boardValue[0])
       if(self.player == "X"):
           totalSum = sumOfX - sumOfO
           #print(sumOfO)
       else:
           totalSum = sumOfO - sumOfX
       return totalSum




   def determineStakeOrRaid(self, newChildNodeAdjMatrix, row, col):
        #print("Row:" + str(row) + "  Column:" + str(col))
        playerInOccupiedCell = newChildNodeAdjMatrix[row][col][1]
        oppPlayer = ""
        moveTypeAndNeighbors = [""]
        if(playerInOccupiedCell == "X"):
            oppPlayer = "O"
        else:
            oppPlayer = "X"
        neighbors = ["","","",""]
        if(row-1>-1 and row-1<self.matrixSize):
            neighbors[0] = newChildNodeAdjMatrix[row-1][col][1]
        else:
            neighbors[0] = "DoesNotExist"
        if (row + 1 > -1 and row + 1 < self.matrixSize):
            neighbors[1] = newChildNodeAdjMatrix[row + 1][col][1]
        else:
            neighbors[1] = "DoesNotExist"
        if (col - 1 > -1 and col - 1 < self.matrixSize):
            neighbors[2] = newChildNodeAdjMatrix[row][col-1][1]
        else:
            neighbors[2] = "DoesNotExist"
        if (col + 1 > -1 and col + 1 < self.matrixSize):
            neighbors[3] = newChildNodeAdjMatrix[row][col+1][1]
        else:
            neighbors[3] = "DoesNotExist"

        if(playerInOccupiedCell in neighbors):
            if(oppPlayer in neighbors):
                indices = [i for i, x in enumerate(neighbors) if x == oppPlayer]
                moveTypeAndNeighbors[0] = "Raid"
                for position in indices:
                    if(position == 0):
                        moveTypeAndNeighbors.append([row - 1,col])
                    if (position == 1):
                        moveTypeAndNeighbors.append([row + 1, col])
                    if (position == 2):
                        moveTypeAndNeighbors.append([row, col - 1])
                    if (position == 3):
                        moveTypeAndNeighbors.append([row, col + 1])
                moveTypeAndNeighbors.append(playerInOccupiedCell)
            else:
                moveTypeAndNeighbors[0] = "Stake"
        else:
            moveTypeAndNeighbors[0] = "Stake"
        return moveTypeAndNeighbors


   def modifyBoard(self, newChildNodeAdjMatrix, positionsToModify):
        playerWhoConquered = positionsToModify[-1]
        #print(positionsToModify)
        for index in range (1,len(positionsToModify)-1):
            row = positionsToModify[index][0]
            col = positionsToModify[index][1]
            newChildNodeAdjMatrix[row][col][1] = playerWhoConquered
        return  newChildNodeAdjMatrix



   def createTree(self):
      #outputFile = open('log.txt', 'w')
      listOfAlphabets = list(string.ascii_uppercase)
      emptyParent1 = TreeNode("NP1","NoParent", "No Parent", 0, "NA", "NA", -2)
      emptyParent2 = TreeNode("NP2", "No Parent", "No Parent", 0, "NA", "NA", -1)
      root = TreeNode("A1", "EmptyParent", self.adjacencyMatrix, 0, "NA", "NA", 0)
      emptyParent2.add_child(root)
      emptyParent1.add_child(emptyParent2)
      masterNode = emptyParent1

      for level in range (0, self.depth):
          noOfParents = len(masterNode.children)
          for parent in range(0,noOfParents):
              parentNode = masterNode.children[parent]
              noOfChildren = len(parentNode.children)
              childNumber = 0
              for child in range(0,noOfChildren):
                  currNode = parentNode.children[child]
                  currNodeAdjMatrix = copy.deepcopy(currNode.data)

                  for index in range(0,self.matrixSize):
                      rowInMatrix = []
                      rowInMatrix = copy.deepcopy(currNodeAdjMatrix[index])
                      sizeOfRow = len(rowInMatrix)
                      for innerIndex in range(0, sizeOfRow):
                          tempNodeAdjMatrix = []
                          tempNodeAdjMatrix = copy.deepcopy(currNodeAdjMatrix)
                          rowInMatrix = []
                          rowInMatrix = copy.deepcopy(tempNodeAdjMatrix[index])
                          boardValues = copy.deepcopy(rowInMatrix[innerIndex])
                          if(boardValues[1] == "~"):
                              childNumber += 1
                              if(level%2 == 0):
                                boardValues[1] = self.player
                                #print("Row:"+str(index)+"  Column:"+str(innerIndex))
                              else:
                                boardValues[1] = self.oppPlayer

                              rowInMatrix[innerIndex] = boardValues
                              tempNodeAdjMatrix[index] = rowInMatrix
                              newChildNodeAdjMatrix = copy.deepcopy(tempNodeAdjMatrix)
                              moveType = self.determineStakeOrRaid(newChildNodeAdjMatrix, index, innerIndex)

                              if(moveType[0] == "Raid"):
                                  utilityValue = self.calculateBoardValue(newChildNodeAdjMatrix)
                                  stakeChildNodeAdjMatrix = copy.deepcopy(newChildNodeAdjMatrix)
                                  colName = listOfAlphabets[innerIndex]
                                  newChildNode = TreeNode(listOfAlphabets[level + 1] + str(childNumber),
                                                          currNode.nodeName, stakeChildNodeAdjMatrix, utilityValue,
                                                          "Stake", colName + str(index + 1), level + 1)
                                  currNode.add_child(newChildNode)
                                  #print(stakeChildNodeAdjMatrix)
                                  #print("\n")

                                  newChildNodeAdjMatrix = copy.deepcopy(self.modifyBoard(newChildNodeAdjMatrix, moveType))
                                  #print(stakeChildNodeAdjMatrix)
                                  #print(newChildNodeAdjMatrix)
                                  utilityValue = self.calculateBoardValue(newChildNodeAdjMatrix)

                                  colName = listOfAlphabets[innerIndex]

                                  newChildNode = TreeNode(listOfAlphabets[level + 1] + str(childNumber),
                                                          currNode.nodeName, newChildNodeAdjMatrix, utilityValue,
                                                          moveType[0], colName + str(index + 1), level + 1)
                                  currNode.add_child(newChildNode)

                              else:
                                  utilityValue = self.calculateBoardValue(newChildNodeAdjMatrix)

                                  colName = listOfAlphabets[innerIndex]

                                  newChildNode = TreeNode(listOfAlphabets[level+1] + str(childNumber), currNode.nodeName, newChildNodeAdjMatrix, utilityValue, moveType[0], colName + str(index+1), level+1)
                                  currNode.add_child(newChildNode)
                              #print(newChildNode.nodeName +" => " + newChildNode.positionOnBoard +" => " +str(newChildNode.utilityValue) + "=>" + newChildNode.moveType + "=>"+ str(newChildNode.parent) + " => " + str(newChildNode.data) + "\n")

                              #outputFile.write(newChildNode.nodeName +" => Depth => " + str(newChildNode.depthOfTree) + " => " + newChildNode.positionOnBoard +" => " +str(newChildNode.utilityValue) + "=>" + newChildNode.moveType + "=>"+ str(newChildNode.parent) + " => " + str(newChildNode.data) + "\n")

          masterNode = parentNode
      #outputFile.close()
      return emptyParent1


   def findMaxOrMin(self, listOfNodes, listOfUtilityValues, currDepthOfTree, finalSelectedNodes):
       listOfTiedNodes = []
       listOfTiedNodesMoveType = []

       if (currDepthOfTree % 2 != 0):
        desiredValue = max(listOfUtilityValues)
       else:
        desiredValue = min(listOfUtilityValues)

       indices = [i for i, x in enumerate(listOfUtilityValues) if x == desiredValue]
       for nodeNo in indices:
           listOfTiedNodes.append(listOfNodes[nodeNo])
           node = listOfNodes[nodeNo]
           listOfTiedNodesMoveType.append(node.moveType)
       if("Raid" in listOfTiedNodesMoveType and "Stake" in listOfTiedNodesMoveType):
           indicesOfStake =  [i for i, x in enumerate(listOfTiedNodesMoveType) if x == "Stake"]
           finalSelectedNodes = listOfTiedNodes[indicesOfStake[0]]
       if("Stake" in listOfTiedNodesMoveType and "Raid" not in listOfTiedNodesMoveType):
           indicesOfStake = [i for i, x in enumerate(listOfTiedNodesMoveType) if x == "Stake"]
           finalSelectedNodes = listOfTiedNodes[indicesOfStake[0]]
       if ("Raid" in listOfTiedNodesMoveType and "Stake" not in listOfTiedNodesMoveType):
           #print("Hello")
           indicesOfRaid = [i for i, x in enumerate(listOfTiedNodesMoveType) if x == "Raid"]
           finalSelectedNodes = listOfTiedNodes[indicesOfRaid[0]]
       return([finalSelectedNodes,desiredValue])



   def calculateMiniMax(self,nodes,currDepthOfTree):
       noOfNodes = len(nodes)
       endOfTree = 0
       finalValues = []
       maxValue = []
       listOfNodes = []
       finalListOfNodes = []
       currDepthOfTree += 1
       for node in range(0,noOfNodes):
            currNode = nodes[node]
            listOfChildren = currNode.children
            if len(listOfChildren) != 0:
                endOfTree = 0
                maxMinList = self.calculateMiniMax(listOfChildren, currDepthOfTree)
                finalListOfNodes = copy.deepcopy(maxMinList[0])
                listOfNodes.append(currNode)
                maxValue.append(maxMinList[1])
                #print(str(currDepthOfTree) + " => " + currNode.nodeName + " => "+ str(maxValue))
            else:
                endOfTree = 1
                listOfNodes.append(currNode)
                finalValues.append(currNode.utilityValue)
                #print(str(currDepthOfTree) + "=>" +currNode.nodeName + " => " + str(finalValues))
       if endOfTree == 1:
           if (currDepthOfTree % 2 != 0):
               return (self.findMaxOrMin(listOfNodes, finalValues, currDepthOfTree, finalListOfNodes))
           else:
               return (self.findMaxOrMin(listOfNodes, finalValues, currDepthOfTree, finalListOfNodes))
       else:
           if(currDepthOfTree%2 != 0):
            return (self.findMaxOrMin(listOfNodes, maxValue, currDepthOfTree, finalListOfNodes))
           else:
            return (self.findMaxOrMin(listOfNodes, maxValue, currDepthOfTree, finalListOfNodes))



   def writeToOutputFile(self, resultNode):
       outputFile = open('output.txt', 'w')
       outputFile.write(resultNode.positionOnBoard + " " + resultNode.moveType)
       outputFile.write("\n")
       adjMatrix = resultNode.data
       for row in range(0,self.matrixSize):
           for col in range(0,self.matrixSize):
               if(adjMatrix[row][col][1] == "~"):
                   outputFile.write(".")
               else:
                   outputFile.write(adjMatrix[row][col][1])
           outputFile.write("\n")



   def minimaxAlgo2(self, emptyParent1):
       emptyParent2 = emptyParent1.children[0]
       root = emptyParent2.children[0]
       maxValue = self.calculateMiniMax([root],-1)
       #print(maxValue[0].nodeName)
       resultNode = maxValue[0]
       self.writeToOutputFile(resultNode)








   def selectStakeOverRaid(self,tiedNodes):
       #tiedUtilityValueNodes = 0
       listOfMatchedNodes = []
       finalSelectedNode = []
       listOfMatchedNodesMoveType = []

       firstMatchedNode = tiedNodes[0]
       listOfMatchedNodes.append(firstMatchedNode)
       listOfMatchedNodesMoveType.append(firstMatchedNode.moveType)
       sizeOfTiedNodes = len(tiedNodes)
       for index in range (1,sizeOfTiedNodes):
           if(firstMatchedNode.utilityValue == tiedNodes[index].utilityValue):
               listOfMatchedNodes.append(tiedNodes[index])
               listOfMatchedNodesMoveType.append(tiedNodes[index].moveType)

       if ("Raid" in listOfMatchedNodesMoveType and "Stake" in listOfMatchedNodesMoveType):
           indicesOfStake = [i for i, x in enumerate(listOfMatchedNodesMoveType) if x == "Stake"]
           finalSelectedNode = listOfMatchedNodes[indicesOfStake[0]]
       if ("Stake" in listOfMatchedNodesMoveType and "Raid" not in listOfMatchedNodesMoveType):
           indicesOfStake = [i for i, x in enumerate(listOfMatchedNodesMoveType) if x == "Stake"]
           finalSelectedNode = listOfMatchedNodes[indicesOfStake[0]]
       if ("Raid" in listOfMatchedNodesMoveType and "Stake" not in listOfMatchedNodesMoveType):
           indicesOfRaid = [i for i, x in enumerate(listOfMatchedNodesMoveType) if x == "Raid"]
           finalSelectedNode = listOfMatchedNodes[indicesOfRaid[0]]
       return (finalSelectedNode)






   def calculateMiniMaxOrAlphaBeta(self, node, currDepthOfTree, isAlphaBetaEnabled):
       alpha = -100000000
       beta = 100000000
       alpha = self.traverseTree2(alpha, beta, node, currDepthOfTree, isAlphaBetaEnabled, [])
       selectedNode = 0
       tiedNodes = []
       #print("\n")
       #print(alpha)
       #print(alpha[0])
       #print(alpha[1])

       #for list in alpha[1]:
       #    print(list[0].nodeName)
       #    print(list[1])
       #    print("\n")


       for innerList in alpha[1]:
           #print(innerList[0].nodeName + "    " + str(innerList[1]))
           if(innerList[1] == alpha[0]):
               #selectedNode = innerList[0]
               tiedNodes.append(innerList[0])
               #print(("Selected Node :" + selectedNode.nodeName))

       selectedNode = self.selectStakeOverRaid(tiedNodes)
       return selectedNode





   def traverseTree2(self,alpha, beta, node, currDepthOfTree, isAlphaBetaEnabled, listOfLevel1Nodes):
       currNode = node
       currDepthOfTree = currNode.depthOfTree
       if currDepthOfTree % 2 == 0:
           v = -100000000
       else:
           v = 100000000

       childrenOfCurrNode = currNode.children

       if (len(childrenOfCurrNode) == 0):
           if currDepthOfTree % 2 == 0:
               if currNode.utilityValue > v:
                   v = currNode.utilityValue
               if v > alpha:
                   alpha = v

               if currDepthOfTree == 1:
                   doesExist = "False"
                   sizeOfList = len(listOfLevel1Nodes)
                   for index in range(0,sizeOfList):
                       innerList = listOfLevel1Nodes[index]
                       if innerList[0] == currNode:
                           innerList[1] = beta
                           doesExist = "True"
                           listOfLevel1Nodes[index] = innerList
                           break
                   if(doesExist == "False"):
                        listOfLevel1Nodes.append([currNode,beta])
               return [alpha,listOfLevel1Nodes]
           else:
               if currNode.utilityValue < v:
                   v = currNode.utilityValue
               if v < beta:
                   beta = v
               if currDepthOfTree == 1:
                   doesExist = "False"
                   sizeOfList = len(listOfLevel1Nodes)
                   for index in range(0,sizeOfList):
                       innerList = listOfLevel1Nodes[index]
                       if innerList[0] == currNode:
                           innerList[1] = beta
                           doesExist = "True"
                           listOfLevel1Nodes[index] = innerList
                           break
                   if(doesExist == "False"):
                        listOfLevel1Nodes.append([currNode,beta])
               return [beta,listOfLevel1Nodes]

       else:
           for child in childrenOfCurrNode:
               [v,listOfLevel1Nodes] = self.traverseTree2(alpha, beta, child, currDepthOfTree, isAlphaBetaEnabled, listOfLevel1Nodes)
               #print(listOfLevel1Nodes)
               #print(child.nodeName + " => " + str(v))
               if currDepthOfTree % 2 == 0:
                   if v > alpha:
                       alpha = v
               else:
                   if v < beta:
                       beta = v
               if currDepthOfTree == 1:
                   doesExist = "False"
                   sizeOfList = len(listOfLevel1Nodes)
                   for index in range(0,sizeOfList):
                       innerList = listOfLevel1Nodes[index]
                       if innerList[0] == currNode:
                           innerList[1] = beta
                           doesExist = "True"
                           listOfLevel1Nodes[index] = innerList
                           break
                   if(doesExist == "False"):
                        listOfLevel1Nodes.append([currNode,beta])
               #for innerList in listOfLevel1Nodes:
               #    print("Hello  "+ innerList[0].nodeName + "    " + str(innerList[1]))
               if isAlphaBetaEnabled:
                   if currDepthOfTree % 2 == 0:
                       if alpha >= beta:
                           return [beta,listOfLevel1Nodes]
                   else:
                       if beta <= alpha:
                           return [alpha,listOfLevel1Nodes]

           if currDepthOfTree % 2 == 0:
               if v > alpha:
                   alpha = v
               return [alpha,listOfLevel1Nodes]
           else:
               if v < beta:
                   beta = v
               return [beta,listOfLevel1Nodes]





   def alphaBetaAlgo(self, emptyParent1):
       emptyParent2 = emptyParent1.children[0]
       root = emptyParent2.children[0]
       resultNode = self.calculateMiniMaxOrAlphaBeta(root, root.depthOfTree, 1)
       #print(resultNode)
       # print(maxValue[0].nodeName)
       #resultNode = maxValue[0]
       #print(resultNode.nodeName)
       self.writeToOutputFile(resultNode)


   def minimaxAlgo(self, emptyParent1):
       emptyParent2 = emptyParent1.children[0]
       root = emptyParent2.children[0]
       resultNode = self.calculateMiniMaxOrAlphaBeta(root, root.depthOfTree, 0)
       print(resultNode)
       # print(maxValue[0].nodeName)
       #resultNode = maxValue[0]
       #print(resultNode.nodeName)
       self.writeToOutputFile(resultNode)







   def startGame(self, emptyParent1):
       if self.algo == "MINIMAX":
           self.minimaxAlgo2(emptyParent1)
           #self.minimaxAlgo2(emptyParent1)
       if self.algo == "ALPHABETA":
           self.alphaBetaAlgo(emptyParent1)






   def mainFunction(self):
       self.readInputFileAndCreateMatrix()
       emptyParent1 = self.createTree()
       self.startGame(emptyParent1)



homework2().mainFunction()
