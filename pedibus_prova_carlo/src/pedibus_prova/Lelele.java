package pedibus_prova;

import java.util.ArrayList;

public class Lelele {
	public static void main(String[] args) {
		
		//VARIABLES
		final int NODES = 5;
		final double ALPHA = 1.46;
		Point[] points = new Point[NODES+1];
		points[0]= new Point(46,31);
		points[1]= new Point(34,19);
		points[2]= new Point(55,54);
		points[3]= new Point(46,16);
		points[4]= new Point(57,42);
		points[5]= new Point(27,16);
		
		int pathNumber;
		ArrayList<Integer> path = new ArrayList<Integer>();
		
		//DISTANCE MATRIX
		double[][] distance = new double [NODES+1][NODES+1];
		for(int i=0; i<NODES+1; i++){
			for(int j=0; j<NODES+1; j++){
				if(i!=j){		
				distance[i][j] = points[i].distanceTo(points[j]); 
				System.out.println("distance from " + (i) + " to " + (j) + " is " + distance[i][j]);
				}
			}
		}
		
		//ogni nodo del path deve essere < di alpha*d(n,root)
		//5-1-0
		System.out.println("path "+(distance[5][1] + distance[1][0])+" alpha "+(ALPHA*(distance[5][0]+distance[1][0])));
		if((distance[5][1] + distance[1][0]) < ALPHA*(distance[5][0]+distance[1][0]))
			{
				System.out.println("5-1-0 path possibile");
			}
		else System.out.println("5-1-0 path not possible");

		//5-1-2-3-0
		System.out.println("path "+(distance[5][1] + distance[1][2] + distance[2][3] + distance[3][0])+" alpha "+(ALPHA*(distance[5][0]+distance[1][0]+distance[2][0]+distance[3][0])));
		if((distance[5][1] + distance[1][2] + distance[2][3] + distance[3][0]) < ALPHA*(distance[5][0]+distance[1][0]+distance[2][0]+distance[3][0]))
		{
			System.out.println("5-1-2-3-0 path possibile");
		}
	else System.out.println("5-1-2-3-0 path not possible");
	
				
		System.out.println("\nsuca");
	}

}
