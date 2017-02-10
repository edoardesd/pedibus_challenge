package pedibus_prova;


public class Lelele {
	public static void main(String[] args) {
		
		//VARIABLES
		final int NODES = 5;
		final double ALPHA = 1.46;
		Point root = new Point(46, 31);
		
		Point[] points = new Point[NODES];
		points[0]= new Point(34,19);
		points[1]= new Point(55,54);
		points[2]= new Point(46,16);
		points[3]= new Point(57,42);
		points[4]= new Point(27,16);
		
		double[][] distances = new double [NODES][NODES];
		for(int i=0; i<NODES; i++){
			for(int j=0; j<NODES; j++){
				if(i!=j){
				distances[i][j] = points[i].distanceTo(points[j]); 
				System.out.println("distance from " + (i+1) + " to " + (j+1) + " is " + distances[i][j]);
				}
			}
			double point_root = root.distanceTo(points[i]);
			System.out.println("distance from " + (i+1) + " to root " + " is " + point_root);
		}
		
		System.out.println("\nsuca");
	}

}
