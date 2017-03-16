#include <iostream>
#include <algorithm>
#include <cstring>
#include <stdio.h>
#include <time.h>
#include <vector>
using namespace std;

//extern "C" {
int HR[32487834];
int calcs[13] = {0,0,0,0,0,0,0,0,0,0,0,0,0};
int vsuits[4] = {0, 1, 2, 3};
int specialsuits[4] = {0,0,0,0};
int myhandstr;
int win, hands, countdeck;
int oc1, oc2;
int * heads_up;
float value, outvalue;
std::vector<int> suits(&vsuits[0], &vsuits[0]+4);
std::vector<int> newboard, allcards(7);

int InitTheEvaluator()
{
    memset(HR, 0, sizeof(HR));
    FILE * fin = fin = fopen("C:\\Users\\QQ\\Dropbox\\poker bot\\evaluators\\HandRanks.dat", "rb");
    size_t bytesread = fread(HR, sizeof(HR), 1, fin);
    fclose(fin);
}

int GetHandValue(vector<int> pCards)
{
	int p = 53;
	for (int i = 0; i < 7; i++)
	{
		p = HR[p + pCards[i]];
		if(pCards[i] == 0) break;
	}
	return p;
}

void setOppCards(int *oppcards, int size)
{
    heads_up = new int [size];
    for (int i=0; i<size; i++)
    {
        heads_up[i] = oppcards[i];
    }
}

float cardodds(vector<int> board, vector<int> mycards)
{

    if (board.size() < 5)
        board.push_back(0);
    mycards.insert(mycards.end(), board.begin(), board.end());
    myhandstr = GetHandValue(mycards);
    win = 0;
    hands = 0;
    for (int i=0; i<sizeof(heads_up)/sizeof(heads_up[0]); i+2)
    {
        std::random_shuffle(suits.begin(), suits.end() );
        if (heads_up[i] % 4 == heads_up[i+1] % 4)
        {
            oc1 = heads_up[i]+suits[0];
            oc2 = heads_up[i+1]+suits[0];
        }
        else
        {
            oc1 = (heads_up[i]/4*4)+1 + suits[0];
            oc2 = (heads_up[i+1]/4*4)+1 + suits[1];
        }
        if (std::find(mycards.begin(), mycards.end(), oc1) != mycards.end()) continue;
        else if (std::find(mycards.begin(), mycards.end(), oc2) != mycards.end()) continue;
        else
        {
            allcards[0] = oc1;
            allcards[1] = oc2;
            for (int i=0; i<board.size(); i++)
            {
                allcards[i+2] = board[i];
            }
        }
        if (GetHandValue(allcards) <= myhandstr)
        {
            win += 1;
        }
        hands += 1;
    }
    return float(win)/float(hands);
}

float cardouts(vector<int> board, vector<int> mycards)
{
    for (int i=0; i<board.size(); i++)
    {
        specialsuits[board[i] % 4] += 1;
    }

    outvalue = 0;
    countdeck = 0;
    for (int i=1; i<53; i++)
    {
        if (std::find(mycards.begin(), mycards.end(), i) != mycards.end()) continue;
        else if (std::find(board.begin(), board.end(), i) != board.end()) continue;
        countdeck++;
        newboard = board;
        newboard.push_back(i);

        if (specialsuits[i%4] > 1)
        {
            value = cardodds(newboard, mycards);
        }
        else if (calcs[i/4] == 0) {
            value = cardodds(newboard, mycards);
            calcs[i/4] = value;
        }
        else
        {
            value = calcs[i/4];
        }
        outvalue += value;

    }
    return float(outvalue)/float(countdeck);
}
int main()
{
    int oppcards[169*2] = {49, 50, 45, 46, 41, 42, 37, 38, 33, 34, 29, 30, 25, 26, 45, 49, 21, 22, 41, 49, 46, 49, 37, 49, 42, 49, 33, 49, 17, 18, 38, 49, 41, 45, 29, 49, 34, 49, 37, 45, 25, 49, 42, 45, 33, 45, 13, 14, 29, 50, 21, 49, 37, 46, 37, 41, 34, 45, 29, 45, 25, 50, 17, 49, 13, 49, 33, 41, 21, 50, 9, 49, 37, 42, 29, 46, 25, 45, 5, 49, 29, 41, 33, 37, 34, 41, 9, 10, 17, 50, 21, 45, 13, 50, 1, 49, 17, 45, 9, 50, 25, 41, 25, 46, 29, 37, 13, 45, 29, 42, 5, 50, 34, 37, 21, 46, 5, 6, 9, 45, 1, 50, 21, 41, 29, 33, 17, 46, 5, 45, 25, 37, 17, 41, 25, 42, 29, 38, 13, 46, 13, 41, 1, 45, 21, 37, 25, 33, 9, 46, 21, 42, 29, 34, 25, 38, 9, 41, 1, 2, 5, 46, 17, 42, 25, 29, 5, 41, 17, 37, 21, 33, 1, 46, 1, 41, 13, 42, 25, 34, 21, 38, 13, 37, 9, 42, 17, 33, 9, 37, 21, 29, 5, 42, 25, 30, 21, 34, 5, 37, 21, 25, 17, 38, 1, 42, 17, 29, 1, 37, 13, 33, 13, 38, 9, 33, 21, 30, 17, 25, 17, 34, 9, 38, 5, 33, 13, 29, 17, 21, 5, 38, 21, 26, 1, 33, 1, 38, 17, 30, 13, 25, 13, 34, 9, 29, 9, 34, 5, 29, 13, 21, 17, 26, 13, 17, 9, 25, 5, 34, 1, 29, 13, 30, 17, 22, 1, 34, 9, 21, 13, 26, 9, 13, 5, 25, 9, 17, 9, 30, 13, 22, 1, 25, 5, 30, 5, 21, 13, 18, 9, 26, 5, 13, 5, 17, 1, 30, 9, 22, 5, 9, 1, 21, 9, 14, 9, 18, 1, 13, 5, 26, 1, 17, 1, 26, 1, 9, 5, 14, 5, 22, 5, 18, 1, 5, 5, 10, 1, 22, 1, 14, 1, 18, 1, 10, 1, 6};
    setOppCards(oppcards, 169*2);
    int board[3] = {49, 33, 21};
    int mycards[2] = {17, 18};
    std::vector<int> vboard(&board[0], &board[0]+3);
    std::vector<int> vcards(&mycards[0], &mycards[0]+2);
    cout << cardodds(vboard, vcards);
}

