using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental.XR;
using UnityEngine.XR.ARFoundation;
using TMPro;

public class ARLesson : MonoBehaviour
{

    // Variables related to Unity objects
    [SerializeField] private TMP_Text stateText;
    [SerializeField] private TMP_Text planesText;
    [SerializeField] private ARPlaneManager aRPlaneManager;
    [SerializeField] private ARPointCloudManager aRPointCloudManager;
    [SerializeField] private GameObject m_PlacedPrefab;
    [SerializeField] ARSessionOrigin m_SessionOrigin;

    // Variables for this class
    private List<ARPlane> activePlanes = new List<ARPlane>();
    private List<Vector3> activePoints = new List<Vector3>();

    // To handle raycast hits
    static List<ARRaycastHit> s_Hits = new List<ARRaycastHit>();

    // The object instantiated as a result of a successful raycast intersection with a plane.
    public GameObject spawnedObject { get; private set; }

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
        // Update number of planes and cloud points text
        UpdateTextPlanes();

        // Handle screen touches.
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);

            if (m_SessionOrigin.Raycast(touch.position, s_Hits, TrackableType.PlaneWithinPolygon))
            {
                // Raycast hits are sorted by distance, so the first one will be the closest hit.
                var hitPose = s_Hits[0].pose;
                if (spawnedObject == null)
                {
                    spawnedObject = (GameObject)Instantiate(m_PlacedPrefab, hitPose.position, hitPose.rotation);
                }
                else {
                    // Object already instantiated. Move it at touch position 
                    spawnedObject.transform.position = hitPose.position;
                }
            }
        }
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