using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using TMPro;

public class ARLesson : MonoBehaviour
{

    // Variables related to Unity objects
    [SerializeField] private TMP_Text stateText;
    [SerializeField] private TMP_Text planesText;
    [SerializeField] private ARPlaneManager aRPlaneManager;
    [SerializeField] private ARPointCloudManager aRPointCloudManager;

    // Variables for this class
    private List<ARPlane> activePlanes = new List<ARPlane>();
    private List<Vector3> activePoints = new List<Vector3>();

    // Start is called before the first frame update
    void Start()
    {
        // Update texts at start
        UpdateTextPlanes();

        // Add callbacks
        ARSubsystemManager.systemStateChanged += OnSystemStateChanged;
        aRPlaneManager.planeAdded += OnPlaneAdded;
        aRPlaneManager.planeRemoved += OnPlaneRemoved;
        aRPlaneManager.planeUpdated += OnPlaneUpdated;
        aRPointCloudManager.pointCloudUpdated += OnPointCloudUpdated;
    }

    // Update is called once per frame
    void Update()
    {
        UpdateTextPlanes();
    }

    // Callbacks
    private void OnSystemStateChanged(ARSystemStateChangedEventArgs obj)
    {
        stateText.text = obj.state.ToString();
    }

    private void OnPlaneAdded(ARPlaneAddedEventArgs args)
    {
        if (!activePlanes.Contains(args.plane))
        {
            activePlanes.Add(args.plane);
        }
    }

    private void OnPlaneRemoved(ARPlaneRemovedEventArgs args)
    {
        if (activePlanes.Contains(args.plane))
        {
            activePlanes.Remove(args.plane);
        }
    }

    private void OnPlaneUpdated(ARPlaneUpdatedEventArgs args)
    {
        /* TODO: Code for when two planes merge.
        Tried a lot of things but I could not find how to check which planes merged. 
        Here are some code snippets that I tried but did not work:
        1.  if (args.plane.trackingState == UnityEngine.Experimental.XR.TrackingState.Unavailable)
            {
                activePlanes.Remove(args.plane);
            }
        2.  foreach (ARPlane plane in activePlanes)
            {
                if (plane.trackingState == UnityEngine.Experimental.XR.TrackingState.Unavailable)
                {
                    activePlanes.Remove(plane);
                }
            }
        */
    }

    private void OnPointCloudUpdated(ARPointCloudUpdatedEventArgs args)
    {
        args.pointCloud.GetPoints(activePoints);
    }

    // Function to update the Plane Text
    private void UpdateTextPlanes()
    {
        planesText.text = $"% planes: {activePlanes.Count}\n % points: {activePoints.Count}";
    }
}