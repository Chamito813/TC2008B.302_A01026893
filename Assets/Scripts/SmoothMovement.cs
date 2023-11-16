using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SmoothMovement : MonoBehaviour
{
    [SerializeField] Vector3[] waypoints;
    [Range(0.0f, 1.0f)]
    [SerializeField] float smoothness;

    int currentWaypoint = 0;

    public Vector3[] Waypoints
    {
        get { return waypoints; }
        set { waypoints = value; }
    }

    public float Smoothness
    {
        get { return smoothness; }
        set { smoothness = value; }
    }

    // Nuevo método público para establecer waypoints
    public void SetWaypoints(Vector3[] newWaypoints)
    {
        waypoints = newWaypoints;
        currentWaypoint = 0; // Reiniciar el contador de waypoints
    }

    void Update()
    {
        MoveBetweenWaypoints();
    }

    void MoveBetweenWaypoints()
    {
        if (currentWaypoint < waypoints.Length - 1)
        {
            Debug.Log("Moving between waypoints: " + currentWaypoint + " and " + (currentWaypoint + 1));
            transform.position = Vector3.Lerp(waypoints[currentWaypoint], waypoints[currentWaypoint + 1], smoothness * Time.deltaTime);

            if (Vector3.Distance(transform.position, waypoints[currentWaypoint + 1]) < 0.1f)
            {
                currentWaypoint++;
                Debug.Log("Reached waypoint: " + currentWaypoint);
            }
        }
    }
}