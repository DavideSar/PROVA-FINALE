#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Define file parameters
#define CSV_FILE "log_monitoraggio_25-07-2022.csv"
#define MAX_ROWS 10000
#define MAX_STR 256

// Define sensors names
#define SENSOR_ACC_Y "fridge_black_accel_y"
#define SENSOR_TEMP_AVG "airq_black_temperature"
#define SENSOR_TEMP_PROBE "fridge_black_probe_temperature"

// Trim spaces and newlines
static void trim(char *s)
{
    int start = 0;
    while (s[start] == ' ' || s[start] == '\t')
        start++;
    if (start > 0)
        memmove(s, s + start, strlen(s) - start + 1);

    int end = (int)strlen(s) - 1;
    while (end >= 0 && (s[end] == ' ' || s[end] == '\t' ||
                        s[end] == '\r' || s[end] == '\n'))
    {
        s[end--] = '\0';
    }
}

// Split CSV into each fields
static int split_csv(char *line, char fields[][MAX_STR], int max_fields)
{
    int count = 0;
    char *start = line;
    char *p = line;

    while (*p && count < max_fields)
    {
        if (*p == ',')
        {
            int len = (int)(p - start);
            if (len >= MAX_STR)
                len = MAX_STR - 1;
            strncpy(fields[count], start, len);
            fields[count][len] = '\0';
            trim(fields[count]);
            count++;
            start = p + 1;
        }
        p++;
    }

    if (count < max_fields)
    {
        strncpy(fields[count], start, MAX_STR - 1);
        fields[count][MAX_STR - 1] = '\0';
        trim(fields[count]);
        count++;
    }
    return count;
}

static double get_mean(double *data, int n)
{
    double sum = 0.0;
    for (int i = 0; i < n; i++)
        sum += data[i];
    return sum / n;
}

static double get_variance(double *data, int n)
{
    double mean = get_mean(data, n);
    double sum = 0.0;
    for (int i = 0; i < n; i++)
    {
        double diff = data[i] - mean;
        sum += diff * diff;
    }
    return sum / n;
}

static double get_std(double *data, int n)
{
    return sqrt(get_variance(data, n));
}

// Standard error on mean
static double get_sem(double *data, int n)
{
    return get_std(data, n) / sqrt((double)n);
}

// qsort comparator for doubles
static int cmp_double(const void *a, const void *b)
{
    double da = *(const double *)a;
    double db = *(const double *)b;
    if (da < db)
        return -1;
    if (da > db)
        return 1;
    return 0;
}

static double get_median(double *data, int n)
{
    double tmp[MAX_ROWS];
    memcpy(tmp, data, n * sizeof(double));
    qsort(tmp, n, sizeof(double), cmp_double);

    double median;
    if (n % 2 == 0)
        median = (tmp[n / 2 - 1] + tmp[n / 2]) / 2.0;
    else
        median = tmp[n / 2];

    return median;
}

static double get_mode(double *data, int n)
{
    double tmp[MAX_ROWS];
    for (int i = 0; i < n; i++)
        tmp[i] = round(data[i] * 1000.0) / 1000.0;
    qsort(tmp, n, sizeof(double), cmp_double);

    double mode = tmp[0];
    int max_count = 1;
    int cur_count = 1;

    for (int i = 1; i < n; i++)
    {
        if (tmp[i] == tmp[i - 1])
        {
            cur_count++;
            if (cur_count > max_count)
            {
                max_count = cur_count;
                mode = tmp[i];
            }
        }
        else
        {
            cur_count = 1;
        }
    }
    return mode;
}

static int remove_anomalies(double *src, int n, double *dst)
{
    double mean = get_mean(src, n);
    double std = get_std(src, n);
    int out = 0;
    for (int i = 0; i < n; i++)
    {
        if (fabs(src[i] - mean) < 2.0 * std)
        {
            dst[out++] = src[i];
        }
    }
    return out;
}

static void print_stats(double *data, int n, const char *name)
{
    printf("Sensore: %s\n", name);
    printf("  Media................%.3f\n", get_mean(data, n));
    printf("  Mediana..............%.3f\n", get_median(data, n));
    printf("  Moda.................%.3f\n", get_mode(data, n));
    printf("  Varianza.............%.3f\n", get_variance(data, n));
    printf("  STD..................%.3f\n", get_std(data, n));
    printf("  Err std su media.....%.3f\n", get_sem(data, n));
    printf("\n");
}

static void print_stats_on_file(FILE *file, double *data, int n, const char *name)
{
    fprintf(file, "Sensore: %s\n", name);
    fprintf(file, "  Media................%.3f\n", get_mean(data, n));
    fprintf(file, "  Mediana..............%.3f\n", get_median(data, n));
    fprintf(file, "  Moda.................%.3f\n", get_mode(data, n));
    fprintf(file, "  Varianza.............%.3f\n", get_variance(data, n));
    fprintf(file, "  STD..................%.3f\n", get_std(data, n));
    fprintf(file, "  Err std su media.....%.3f\n", get_sem(data, n));
    fprintf(file, "\n");
}

int main(void)
{

    // Define CSV filepath
    FILE *file = fopen(CSV_FILE, "r");
    if (!file)
    {
        fprintf(stderr, "Errore: impossibile aprire %s\n", CSV_FILE);
        return 1;
    }

    // Define arrays for raw data
    static double raw_acc_y[MAX_ROWS];
    static double raw_temp_avg[MAX_ROWS];
    static double raw_temp_probe[MAX_ROWS];

    int cnt_acc_y = 0;
    int cnt_temp_avg = 0;
    int cnt_temp_probe = 0;

    int col_time = -1;
    int col_value = -1;
    int col_entity = -1;

    char line[MAX_STR * 10];
    int first_line = 1;

    while (fgets(line, sizeof(line), file))
    {
        // Skip comment lines starting with '#'
        if (line[0] == '#')
        {
            continue;
        }

        char fields[20][MAX_STR];
        int nf = split_csv(line, fields, 20);

        // Parse header to find column positions
        if (first_line)
        {
            first_line = 0;
            for (int i = 0; i < nf; i++)
            {
                if (strcmp(fields[i], "_time") == 0)
                    col_time = i;
                if (strcmp(fields[i], "_value") == 0)
                    col_value = i;
                if (strcmp(fields[i], "entity_id") == 0)
                    col_entity = i;
            }
            if (col_time < 0 || col_value < 0 || col_entity < 0)
            {
                fprintf(stderr, "Errore: colonne mancanti nel CSV.\n");
                fclose(file);
                return 1;
            }
            continue;
        }

        if (nf <= col_value || nf <= col_entity)
        {
            continue;
        }

        // Convert value to double; skip row if conversion fails
        char *endptr;
        double val = strtod(fields[col_value], &endptr);
        if (endptr == fields[col_value])
        {
            continue;
        }

        // Puts row in respective sensor
        char *eid = fields[col_entity];
        if (strcmp(eid, SENSOR_ACC_Y) == 0 && cnt_acc_y < MAX_ROWS)
        {
            raw_acc_y[cnt_acc_y++] = val;
        }
        else if (strcmp(eid, SENSOR_TEMP_AVG) == 0 && cnt_temp_avg < MAX_ROWS)
        {
            raw_temp_avg[cnt_temp_avg++] = val;
        }
        else if (strcmp(eid, SENSOR_TEMP_PROBE) == 0 && cnt_temp_probe < MAX_ROWS)
        {
            raw_temp_probe[cnt_temp_probe++] = val;
        }
    }
    fclose(file);

    // Remove anomalies
    static double clean_acc_y[MAX_ROWS];
    static double clean_temp_avg[MAX_ROWS];
    static double clean_temp_probe[MAX_ROWS];

    int n_acc_y = remove_anomalies(raw_acc_y, cnt_acc_y, clean_acc_y);
    int n_temp_avg = remove_anomalies(raw_temp_avg, cnt_temp_avg, clean_temp_avg);
    int n_temp_probe = remove_anomalies(raw_temp_probe, cnt_temp_probe, clean_temp_probe);

    // Print stats
    printf("Statistiche dei sensori dopo la rimozione delle anomalie:\n\n");
    print_stats(clean_acc_y, n_acc_y, SENSOR_ACC_Y);
    print_stats(clean_temp_avg, n_temp_avg, SENSOR_TEMP_AVG);
    print_stats(clean_temp_probe, n_temp_probe, SENSOR_TEMP_PROBE);

    // Print on log file
    FILE *log_file = fopen("analized_data.log", "w");
    if (log_file == NULL)
    {
        printf("Impossibile aprire o creare il file.\n");
    }
    else
    {
        print_stats_on_file(log_file, clean_acc_y, n_acc_y, SENSOR_ACC_Y);
        print_stats_on_file(log_file, clean_temp_avg, n_temp_avg, SENSOR_TEMP_AVG);
        print_stats_on_file(log_file, clean_temp_probe, n_temp_probe, SENSOR_TEMP_PROBE);
        fclose(log_file);
    }

    return 0;
}