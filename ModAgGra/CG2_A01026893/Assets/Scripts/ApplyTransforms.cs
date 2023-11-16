using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    [SerializeField] Object w1;
    [SerializeField] Object w2;
    [SerializeField] Object w3;
    [SerializeField] Object w4;
    [SerializeField] Vector3 displacement;
    [SerializeField] float rotationSpeed;
    [SerializeField] AXIS rotationAxis;

    SmoothMovement smoothMovement;

    Mesh[] meshes = new Mesh[5];
    Vector3[][] baseVerticesList = new Vector3[5][];
    Vector3[][] newVerticesList = new Vector3[5][];
    

    void Start()
    {
        // Assign meshes to the array
        meshes[0] = GetComponentInChildren<MeshFilter>().mesh;
        meshes[1] = ((GameObject)w1).GetComponentInChildren<MeshFilter>().mesh;
        meshes[2] = ((GameObject)w2).GetComponentInChildren<MeshFilter>().mesh;
        meshes[3] = ((GameObject)w3).GetComponentInChildren<MeshFilter>().mesh;
        meshes[4] = ((GameObject)w4).GetComponentInChildren<MeshFilter>().mesh;

        // Populate baseVertices and newVertices arrays for each mesh
        for (int i = 0; i < meshes.Length; i++)
        {
            baseVerticesList[i] = meshes[i].vertices;
            newVerticesList[i] = new Vector3[baseVerticesList[i].Length];
            for (int j = 0; j < baseVerticesList[i].Length; j++)
            {
                newVerticesList[i][j] = baseVerticesList[i][j];
            }
        }

        // Inicializa la instancia de SmoothMovement con los puntos deseados
        smoothMovement = gameObject.AddComponent<SmoothMovement>();
        Vector3[] newWaypoints = new Vector3[]
        {
            transform.position,
            new Vector3(1.0f, 0.0f, 0.0f),
            new Vector3(1.0f, 0.0f, 1.0f),
            new Vector3(0.0f, 0.0f, 1.0f),
            new Vector3(0.0f, 0.0f, 0.0f), // Regresa a la posición original
        };
        smoothMovement.SetWaypoints(newWaypoints);
        smoothMovement.Smoothness = 0.5f; // Ajusta según sea necesario
    }

    void Update()
    {
       DoTransform();    
    }

    void DoTransform()
    {
        for (int k = 0; k < meshes.Length; k++)
        {
            // Aplica la transformación para la posición (traslación)
            Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time,
                                                            displacement.y * Time.time,
                                                            displacement.z * Time.time);

            Matrix4x4 rotate = HW_Transforms.RotateMat(rotationSpeed * Time.time, rotationAxis);

            Matrix4x4 composite = move;
            if (k > 0)
            {
                composite *= rotate;
            }

            for (int i = 0; i < newVerticesList[k].Length; i++)
            {
                // Transforma la posición (traslación + rotación)
                Vector4 temp = new Vector4(baseVerticesList[k][i].x,
                                            baseVerticesList[k][i].y,
                                            baseVerticesList[k][i].z,
                                            1);

                newVerticesList[k][i] = composite * temp;

            }

            meshes[k].vertices = newVerticesList[k];
            meshes[k].RecalculateNormals();
        }
    }
}
