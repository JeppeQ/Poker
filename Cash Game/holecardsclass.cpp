#include <iostream>
#include <algorithm>
#include <stdlib.h>
#include <vector>  
#include <time.h>

using namespace std;
extern "C" {
    int bucketarray[168][3] = { {12, 12, 0}, {11, 11, 0}, {10, 10, 0}, {9, 9, 0}, {12, 11, 1}, {8, 8, 0}, {7, 7, 0}, {6, 6, 0}, {12, 11, 0}, {12, 10, 0}, {12, 9, 0}, {11, 10, 0}, {11, 9, 0}, {12, 10, 1}, {12, 9, 1}, {11, 10, 1}, {11, 9, 1}, {10, 9, 1}, {5, 5, 0}, {4, 4, 0}, {12, 8, 0}, {12, 7, 0}, {11, 8, 0}, {11, 7, 0}, {10, 9, 0}, {10, 8, 0}, {9, 8, 0}, {8, 7, 0}, {12, 8, 1}, {12, 7, 1}, {11, 8, 1}, {11, 7, 1}, {10, 8, 1}, {10, 7, 1}, {9, 8, 1}, {8, 7, 1}, {7, 6, 1}, {3, 3, 0}, {2, 2, 0}, {1, 1, 0}, {0, 0, 0}, {12, 6, 0}, {12, 5, 0}, {11, 6, 0}, {10, 7, 0}, {9, 7, 0}, {7, 6, 0}, {6, 5, 0}, {5, 4, 0}, {12, 6, 1}, {12, 5, 1}, {12, 4, 1}, {12, 3, 1}, {12, 2, 1}, {12, 1, 1}, {12, 0, 1}, {11, 6, 1}, {11, 5, 1}, {10, 6, 1}, {9, 7, 1}, {8, 6, 1}, {7, 5, 1}, {6, 5, 1}, {6, 4, 1}, {5, 4, 1}, {12, 4, 0}, {12, 3, 0}, {12, 2, 0}, {12, 1, 0}, {12, 0, 0}, {11, 5, 0}, {11, 4, 0}, {11, 3, 0}, {11, 2, 0}, {11, 1, 0}, {11, 0, 0}, {10, 6, 0}, {10, 5, 0}, {10, 4, 0}, {10, 3, 0}, {10, 2, 0}, {10, 1, 0}, {10, 0, 0}, {9, 6, 0}, {9, 5, 0}, {9, 4, 0}, {9, 3, 0}, {9, 2, 0}, {9, 1, 0}, {9, 0, 0}, {8, 6, 0}, {8, 5, 0}, {8, 4, 0}, {8, 3, 0}, {8, 2, 0}, {8, 1, 0}, {8, 0, 0}, {7, 5, 0}, {7, 4, 0}, {7, 3, 0}, {7, 2, 0}, {7, 1, 0}, {7, 0, 0}, {6, 4, 0}, {6, 3, 0}, {6, 2, 0}, {6, 1, 0}, {6, 0, 0}, {5, 3, 0}, {5, 2, 0}, {5, 1, 0}, {5, 0, 0}, {4, 3, 0}, {4, 2, 0}, {4, 1, 0}, {4, 0, 0}, {3, 2, 0}, {3, 1, 0}, {3, 0, 0}, {2, 1, 0}, {2, 0, 0}, {1, 0, 0}, {11, 4, 1}, {11, 3, 1}, {11, 2, 1}, {11, 1, 1}, {11, 0, 1}, {10, 5, 1}, {10, 4, 1}, {10, 3, 1}, {10, 2, 1}, {10, 1, 1}, {10, 0, 1}, {9, 6, 1}, {9, 5, 1}, {9, 4, 1}, {9, 3, 1}, {9, 2, 1}, {9, 1, 1}, {9, 0, 1}, {8, 5, 1}, {8, 4, 1}, {8, 3, 1}, {8, 2, 1}, {8, 1, 1}, {8, 0, 1}, {7, 4, 1}, {7, 3, 1}, {7, 2, 1}, {7, 1, 1}, {7, 0, 1}, {6, 3, 1}, {6, 2, 1}, {6, 1, 1}, {6, 0, 1}, {5, 3, 1}, {5, 2, 1}, {5, 1, 1}, {5, 0, 1}, {4, 2, 1}, {4, 1, 1}, {4, 0, 1}, {3, 2, 1}, {3, 1, 1}, {3, 0, 1}, {2, 1, 1}, {2, 0, 1}, {1, 0, 1} };
    int cardrank[13] = {0};
    int cardsuit[4] = {0};
	int cards[20];
	int a[5] = { 0 };
	int bcardinfo[2][5];
// Set bucketBound for bucketing

void setSeed(){
    	srand (time(NULL));
}
int bucketBound(double bound){
    if (bound <= 0.3)
        return 4;
    else if (bound <= 0.10)
    	return 17;
	else if (bound <= 0.21)
		return 36;
	else if (bound <= 0.35)
		return 64;
	else
		return 167;
}
//Following functions determine the amount of Toppairs and Nutcards given out in the simulation
//Based on foldratio from state 2 (post-flop)
int pTop(double foldratio) {
    if (foldratio < 0.33)
		return int((0.33 * ((foldratio / 0.33)*(foldratio / 0.33)))*100);
    else
		return int(0.33*100); }

int pNut(double foldratio) {
	if (foldratio < 0.33)
		return 0;
	else if (0.33 <= foldratio < 0.66)
		return int((0.33 * ((foldratio - 0.33)/0.33)*((foldratio - 0.33)/0.33))*100);
	else
		return int((foldratio - 0.33)*100);
}

// Finds the next available card starting from xcard, either decreasing(s = -1) or ascending(s = 1)
int findNext(int xcard, int s){
	for (int q = 0; q < (sizeof(cards)/sizeof(*cards)); q++){
			if (cards[q] == xcard){
				xcard += s;
				q = -1;
			}
	}
	return xcard;
}
// Return a randomcard from the possible cards
int randomCard(){
	int r = rand() % 52;
	for (int q = 0; q < (sizeof(cards)/sizeof(*cards)); q++){
		if (cards[q] == r){
			r = rand() % 52;
			q = -1; }
	}
	return r;
}
// Return card to make a pair, else highest card
int topPair(int bcardl){
	for (int i = bcardl-1; i >= 0; i--) {
		if (cardrank[bcardinfo[0][i]] < 4)
			return findNext(bcardinfo[0][i]*4, 1);
	}
	return findNext(51, -1);
}
// Return card to make pair, else -1   
int pairOrNothing(int bcardl){
	for (int i = bcardl-1; i >= 0; i--) {
		if (cardrank[bcardinfo[0][i]] < 4)
			return findNext(bcardinfo[0][i]*4, 1);
	}
	return -1;
}
// Returns a card in the same suit as the scard given
int sameSuit(int scard){
	for (int q = 0; q < (sizeof(cards)/sizeof(*cards)); q++){
			if (cards[q] == scard){
				scard -= 4;
				q = -1;
			}
	}
	return scard;
}
// Returns a card in the same rank as rcard or None
int sameRank(int rcard){
	if (cardrank[rcard] < 4)
		return findNext(rcard*4, 1);
	return -1;
}
// Used in bucketing for suited cards
bool cardAvailable(int card) {
	for (int q = 0; q < (sizeof(cards)/sizeof(*cards)); q++){
			if (cards[q] == card)
				return false;
	}
	return true;
}

//Returns a random selected bucket from the bucketarray
void bucketing(int cf, double fr, double cr, int f, int second){
	int uber, lower, i, first, rb;
	if (cf == 2){
		uber = 0;
		lower = bucketBound(1-(fr+cr));
	}
	else if (cf == 1){
		uber = bucketBound(1-(fr+cr));
		lower = bucketBound(fr);
	}

	while(true){
		rb = rand() % (max(uber,lower)-min(uber,lower)) + min(uber,lower);
		if (bucketarray[rb][2] == 1){
			if (cardrank[bucketarray[rb][0]] < 4 && cardrank[bucketarray[rb][1]]){
				for (i = 0; i < 4; i++) {
					if (cardAvailable(bucketarray[rb][0]*4+i) && cardAvailable(bucketarray[rb][1]*4+i)){
						cards[f] = bucketarray[rb][0]*4+i;
						cards[second] = bucketarray[rb][1]*4+i;
                        break;
					}
				}
			}
		}
		else if (bucketarray[rb][2] == 0){
			if (bucketarray[rb][0] == bucketarray[rb][1] && cardrank[bucketarray[rb][0]] < 3){
				cards[f] = findNext(bucketarray[rb][0]*4, 1);
				cards[second] = findNext(cards[f]+1, 1);
                break;
			}
			else if (bucketarray[rb][0] != bucketarray[rb][1] && cardrank[bucketarray[rb][0]] < 4 && cardrank[bucketarray[rb][1]] < 4){
				cards[f] = findNext(bucketarray[rb][0]*4,1);
				cards[second] = findNext(bucketarray[rb][1]*4,1);
                break;
			}
		}
	}
}

// Find the sum of unique number in bcardinfo ranks
int uniquesum(int len){
    int sum = 0;
	for (int i = 0; i < len-1; i++) {
		if (bcardinfo[0][i] == bcardinfo[0][i+1])
			continue;
		if (i == len-2)
			sum += bcardinfo[0][i+1];
		sum += bcardinfo[0][i];
	}
    return sum;
}
// Used in checkStraight
int sumplus(int len){
    int sum = 0;
	for (int i = 0; i < 3; i++) {
		sum += bcardinfo[0][i];
	}
    return sum+12;
}
// Used in checkStraight
int addNumbers(int range, int start){
	int sum = 0;
	for (int i = 0; i <= range; i++){
		sum += start - i;
	}
    return sum;
}


// Check if there is straight possibility
int checkStraight(int a[5],int blen){
	if (a[1] > 3){
		if (bcardinfo[0][blen-1] == 12){
			if (bcardinfo[0][3] < 4)
				return sameRank(18 - uniquesum(blen));
			else if (blen == 4 && bcardinfo[0][2] < 4)
				return sameRank(18 - uniquesum(blen));
			else if (a[1] > 4 && bcardinfo[0][2] < 4)
				return sameRank(18 - sumplus(blen));
		}
		if (blen == 4 && bcardinfo[0][3]-bcardinfo[0][0] < 4){
			if (bcardinfo[0][3] < 12 && cardrank[bcardinfo[0][3]+1] < 4)
				return findNext((bcardinfo[0][3]+1)*4, 1);
			else if (bcardinfo[0][0] > 0 && cardrank[bcardinfo[0][0]-1] < 4)
				return findNext((bcardinfo[0][0]-1)*4, 1); }
		else if (blen == 4 && bcardinfo[0][3]-bcardinfo[0][0] < 5)
			return sameRank(addNumbers(4, bcardinfo[0][3]) - uniquesum(blen));
		else if (a[1] > 4 && bcardinfo[0][4]- bcardinfo[0][0] < 5){
             if (bcardinfo[0][4] < 12 && cardrank[bcardinfo[0][4]+1] < 4)
				return findNext((bcardinfo[0][4]+1)*4, 1);
			else if (bcardinfo[0][0] > 0 && cardrank[bcardinfo[0][0]-1] < 4)
				return findNext((bcardinfo[0][0]-1)*4, 1);
             }
		else if (a[1] > 4 && bcardinfo[0][3]- bcardinfo[0][0] < 4){
			if (bcardinfo[0][3] < 12 && cardrank[bcardinfo[0][3]+1] < 4)
				return findNext((bcardinfo[0][3]+1)*4, 1);
			else if (bcardinfo[0][0] > 0 && cardrank[bcardinfo[0][0]-1] < 4)
				return findNext((bcardinfo[0][0]-1)*4, 1);
		}
		else if (a[1] > 4 && bcardinfo[0][4] - bcardinfo[0][1] < 4) {
			if (bcardinfo[0][4] < 12 && cardrank[bcardinfo[0][4]+1] < 4)
				return findNext((bcardinfo[0][4]+1)*4, 1);
			else if (bcardinfo[0][1] > 0 && cardrank[bcardinfo[0][1]-1] < 4)
				return findNext((bcardinfo[0][1]-1)*4, 1);
		}
		else if (blen == 5 && bcardinfo[0][4] - bcardinfo[0][0] < 5)
			return sameRank(addNumbers(4, bcardinfo[0][4]) - uniquesum(blen));
		else if (a[1] > 4 && blen == 5 && bcardinfo[0][3] - bcardinfo[0][0] < 5)
			return sameRank(addNumbers(4, bcardinfo[0][3]) - (uniquesum(blen)-bcardinfo[0][4]));
		else if (blen == 5 && a[1] > 4 && bcardinfo[0][4] - bcardinfo[0][1] < 5)  
			return sameRank(addNumbers(4, bcardinfo[0][4]) - (uniquesum(blen)-bcardinfo[0][0]));
		}
	return -1;
	}
// Return Nut Card (Best possible card)
int nutCard(int len, int identicard, int maxbrank, int countsuits, int maxsuitindex) {
	int index;

	//Check four of a kind
	if (identicard == 3 && cardrank[maxbrank] == 3)
		return findNext(maxbrank*4, 1);
	
	if (len > 3){
		//Check full-house
		if (identicard > 1){
			if (a[2] > 1 || identicard > 2)
				if (identicard == 3){
					index = pairOrNothing(len);
					if (index != -1)
						return index;
				}
		}	
		//Check flush
		if (countsuits > 3){
			if (cardsuit[maxsuitindex] < 13)
				return sameSuit(maxsuitindex + 48);
		}
		//Check straight
		index = checkStraight(a, len);
		if (index != -1)
			return index;
	}
	// Three of a kind
	if (identicard == 2){
		if (a[2] >= 1 && cardrank[maxbrank] < 4)
			return findNext(maxbrank*4, 1);
	}
	// pair or high card
	return topPair(len);
	
}

//Main function, which returns a list of simulated cards
int *holeCards(int hands, int hcards[2], int bcards[], double ratios[3], int cf, int len) {
	int gcard, rcard, precards, bcardlength, i, h;
	int Top, Nut, nummer, identicard = 1, maxbrank, tmp = 1, countsuits = 1, maxsuitindex, tmp2 = 1;
	bcardlength = len;

    for (h = 0; h < sizeof(cards)/sizeof(*cards); h++)
        cards[h] = -1;
    for (h = 0; h < 13; h++)
        cardrank[h] = 0;
    for (h = 0; h < 4; h++)
        cardsuit[h] = 0;
    for (h = 0; h < 5; h++)
        a[h] = 0;
	
	//Sort the board cards, and get their ranks and suits
	for (i = 0; i < bcardlength; i++){
		bcardinfo[0][i] = bcards[i]/4;
		bcardinfo[1][i] = bcards[i]%4;
	}
	precards = bcardlength + 2;

	//Add the known cards to the lists over used cards
	for (i = 0; i < precards; i++){
		if (i < bcardlength){
			cards[i+hands*2] = bcards[i];
			cardrank[bcards[i]/4] += 1;
			cardsuit[bcards[i]%4] += 1;
		}
		else{
			cards[i+hands*2] = hcards[i-bcardlength];
			cardrank[hcards[i-bcardlength]/4] += 1;
			cardsuit[hcards[i-bcardlength]%4] += 1;
		}
	}

    // Find highest number of identical cards, its index(maxbrank) and find occurences of identical cards [a]
    for (i = 0; i < len-1; i++) {
		if (bcardinfo[0][i] == bcardinfo[0][i+1]) {
			tmp+=1;
            if (i+1 == len-1)
				a[tmp] += 1;
			if (tmp >= identicard ) {
				identicard = tmp;
				maxbrank = bcardinfo[0][i]; 
			}
		}
		else {
			if (i+1 == len-1)
				a[tmp] += 1;
			a[tmp] += 1;
			tmp = 1;
		}
		// same for bsuit
		if (bcardinfo[1][i] == bcardinfo[1][i+1]) {
			tmp2+=1;
			if (tmp2 >= countsuits) {
				countsuits = tmp2;
				maxsuitindex = bcardinfo[1][i]; 
			}
		}
		else {
			tmp2 = 1;
		}
	}
    
	//Main loop which select cards
	for (i = 0; i < hands; i++) {
		//Update the cardrank and cardsuit array if some cards have been dealt
		if (i > 0){
			for (int a = 0; a < 2; a++){
				cardrank[cards[(i-1)*2+a]/4] += 1;
				cardsuit[cards[(i-1)*2+a]%4] += 1;
			}
		}
		//ratios[3][i] is the fold ratio of player post-flop
		Top = pTop(ratios[i]);
		Nut = pNut(ratios[i]);
		//Random number to determine which cards will be dealt
		nummer = rand()%100;
		// Assign top pair(gcard) and random card(rcard)
		if (nummer <= Top){
			gcard = topPair(bcardlength);
			cards[i*2] = gcard;
			rcard = randomCard();
			cards[i*2+1] = rcard;
		}
		// Assign nut card and random card
		else if (Top < nummer < Nut+Top) {
			gcard = nutCard(bcardlength, identicard, maxbrank, countsuits, maxsuitindex);
			cards[i*2] = gcard;
			rcard = randomCard();
			cards[i*2+1] = rcard;
		}
		// Assign cards based on preflop bucket
		else {
			bucketing(cf, ratios[i+hands], ratios[i+hands*2], i*2, i*2+1);
		}	
	}
	rcard = randomCard();
	cards[18] = rcard;
	rcard = randomCard();
	cards[19] = rcard;
return cards;
}
}
